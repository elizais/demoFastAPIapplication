from datetime import datetime
from datetime import timedelta

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .models import RefreshToken
from .schemas import Token
from .schemas import AuthAccount
from ..accounts.models import Accounts
from ..config import Settings
from ..config import get_settings
from ..database import Session
from ..database import get_session
from ..exceptions import EntityDoesNotExistError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/accounts/login')


def get_current_account(
        token: str = Depends(oauth2_scheme),
        settings: Settings = Depends(get_settings),
) -> AuthAccount:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Unauthorized user',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        token_data = jwt.decode(token, settings.secret_key, algorithms=['HS256'])
    except JWTError:
        raise credentials_exception from None

    try:
        return AuthAccount(**token_data.get('account', {}))
    except ValidationError:
        raise credentials_exception from None


class AuthService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.settings = settings

    def authenticate(self, username: str, password: str) -> Token:
        try:
            account = self.session.execute(
                select(Accounts)
                .where(Accounts.username == username)
            ).scalar_one()
        except NoResultFound:
            raise EntityDoesNotExistError from None

        if not pbkdf2_sha256.verify(password, account.password):
            raise EntityDoesNotExistError

        return self.create_tokens_authorization(account)

    def refresh_token_pair(self, refresh_token: str) -> Token:
        try:
            account = self.session.execute(
                select(Accounts)
                .join_from(Accounts, RefreshToken)
                .where(RefreshToken.token == refresh_token)
            ).scalar_one()
        except NoResultFound:
            raise EntityDoesNotExistError from None

        return self.create_tokens_authorization(account)

    def create_tokens_authorization(self, account: Accounts) -> Token:
        access_token = self.create_token(
            account,
            secret_key=self.settings.secret_key,
            lifetime=self.settings.jwt_access_lifetime,
        )
        refresh_token = self.create_token(
            account,
            secret_key=self.settings.secret_key,
            lifetime=self.settings.jwt_refresh_lifetime,
        )

        try:
            account_token = self.session.execute(
                select(RefreshToken)
                .where(RefreshToken.account_id == account.id)
            ).scalar_one()
            account_token.token = refresh_token
        except NoResultFound:
            account_token = RefreshToken(
                account_id=account.id,
                token=refresh_token,
            )
            self.session.add(account_token)

        self.session.commit()

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @classmethod
    def create_token(cls, account: Accounts, *, secret_key: str, lifetime: int) -> str:
        now = datetime.utcnow()
        return jwt.encode({
            'sub': str(account.id),
            'exp': now + timedelta(seconds=lifetime),
            'iat': now,
            'nbf': now,
            'account': {
                'id': account.id,
                'email': account.email,
                'username': account.username,
            },
        }, secret_key, 'HS256')
