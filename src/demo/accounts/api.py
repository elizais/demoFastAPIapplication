from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from ..auth.services import get_current_account
from ..auth.schemas import AuthAccount
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError
from .schemas import Account as AccountSchema
from .schemas import AccountCreate
from .services import AccountService



router = APIRouter(
    prefix='/accounts',
)


@router.post(
    '',
    response_model=AccountSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    account_create: AccountCreate,
    service: AccountService = Depends(),
):
    try:
        account = service.create_account(account_create)
        return account
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT) from None


@router.get('', response_model=List[AccountSchema])
def get_accounts(
    current_account: AuthAccount = Depends(get_current_account),
    service: AccountService = Depends(),
):
    return service.get_accounts()


@router.get('/{account_id}', response_model=AccountSchema)
def get_account(
    account_id: int,
    current_account: AuthAccount = Depends(get_current_account),
    service: AccountService = Depends(),
):
    try:
        return service.get_account(account_id)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None
