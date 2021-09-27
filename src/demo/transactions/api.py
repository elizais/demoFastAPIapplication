from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from .schemas import Transaction
from .schemas import TransactionCreate
from .services import TransactionsService
from .services import TransactionGetQuery
from ..auth.services import get_current_account
from ..auth.schemas import AuthAccount
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError

router = APIRouter(
    prefix='/operations'
)


@router.post(
    '',
    response_model=Transaction,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transaction_create: TransactionCreate,
    current_account: AuthAccount = Depends(get_current_account),
    service: TransactionsService = Depends(),
):
    try:
        account = service.create_transaction(transaction_create)
        return account
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT) from None


@router.get(
    '',
    response_model=List[Transaction],
    status_code=status.HTTP_201_CREATED,
)
def get_transaction(
    transactions_get_query: TransactionGetQuery = Depends(),
    current_account: AuthAccount = Depends(get_current_account),
    service: TransactionsService = Depends(),
):
    try:
        transactions = service.get_transactions(transactions_get_query)
        return transactions
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT) from None


@router.get(
    '/report',
    response_model=Transaction,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transactions_get_query: TransactionGetQuery,
    current_account: AuthAccount = Depends(get_current_account),
    service: TransactionsService = Depends(),
):
    try:
        report = service.get_report(transactions_get_query)
        return report
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT) from None
