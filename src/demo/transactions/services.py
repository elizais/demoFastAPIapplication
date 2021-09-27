from collections import Counter
from datetime import date
from typing import List
from typing import Optional
from operator import attrgetter

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from .models import Transactions
from .schemas import TransactionCreate
from .schemas import TransactionGetQuery
from ..config import Settings
from ..config import get_settings
from ..database import Session
from ..database import get_session
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError


class TransactionsService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.settings = settings

    def create_transaction(self, transaction_create: TransactionCreate) -> Transactions:
        transaction = Transactions(
            type=transaction_create.type,
            date=transaction_create.date,
            shop_id=transaction_create.shop_id,
            category_id=transaction_create.category_id,
            name=transaction_create.name,
            price=transaction_create.price,
            amount=transaction_create.amount
        )
        self.session.add(transaction)
        try:
            self.session.commit()
            return transaction
        except IntegrityError:
            raise EntityConflictError from None

    def get_transactions(self, transactions_get_query: Optional[TransactionGetQuery] = None
    ) -> Optional[List[Transactions]]:
        transactions = select(Transactions)
        if transactions_get_query.date_from is not None:
            transactions = transactions.where(
                Transactions.date >= transactions_get_query.date_from
            )
        if transactions_get_query.category is not None:
            transactions = transactions.where(
                Transactions.category_id in transactions_get_query.category
            )
        # self.session.execute().scalars()
        # transactions
        # transactions = self.session.execute(
        #     select(Transactions).where(
        #     )
        # ).scalars().all()
        return self.session.execute(transactions).scalars().all()

#     def get_report(self, transactions_get_query: TransactionGetQuery,):
#         transactions = self.session.execute(self._get_transactions(transactions_get_query)).all()
#         report = {"buy": ReportRecord("buy"), "sale": ReportRecord("sale")}
#         time_points = sorted(list(set(transactions.date)))
#         for row in transactions:
#             row_type = row.type
#             row_date = date.fromisoformat(row.date)
#             row_amount = float(row.amount) * float(row.price)
#             path = [
#                 row.shop,
#                 row.category,
#                 row.name,
#             ]
#             report[row_type].add_row(path, row_date, row_amount)
#             print(report)
#         return {
#             "time_points": time_points,
#             "buy":  {report["buy"]},
#             "sale": {report["sale"]}
#         }
#
#
# class ReportRecord:
#     def __init__(self, key):
#         self.key = key
#         self.amounts = Counter()
#         self.total = 0
#         self.children = {}
#
#     def add_row(self, path, date: str, amount):
#         self.amounts[date] += amount
#         self.total += amount
#
#         if path:
#             key = path.pop(0)
#             try:
#                 child = self.children[key]
#             except KeyError:
#                 child = self.children[key] = ReportRecord(key)
#             child.add_row(path, date, amount)
#
#     def walk(self, level=0):
#         yield level, self
#         for child in sorted(self.children.values(), key=attrgetter('total'), reverse=True):
#             yield from child.walk(level + 1)
