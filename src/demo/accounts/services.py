from typing import List

from fastapi import Depends
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from ..config import Settings
from ..config import get_settings
from ..database import Session
from ..database import get_session
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError
from .models import Accounts
from .schemas import AccountCreate


class AccountService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.settings = settings

    def create_account(self, account_create: AccountCreate) -> Accounts:
        account = Accounts(
            email=account_create.email,
            username=account_create.username,
            password=pbkdf2_sha256.hash(account_create.password),
        )
        self.session.add(account)
        try:
            self.session.commit()
            return account
        except IntegrityError:
            raise EntityConflictError from None

    def get_accounts(self) -> List[Accounts]:
        accounts = self.session.execute(
            select(Accounts)
        ).scalars().all()
        return accounts

    def get_account(self, account_id: int) -> Accounts:
        return self._get_account(account_id)

    def _get_account(self, account_id: int) -> Accounts:
        try:
            account = self.session.execute(
                select(Accounts)
                .where(Accounts.id == account_id)
            ).scalar_one()
            return account
        except NoResultFound:
            raise EntityDoesNotExistError from None
