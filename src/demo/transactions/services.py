from collections import Counter
from datetime import date
from typing import List
from typing import Optional
from operator import attrgetter

from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import aliased
from sqlalchemy.sql import join

from .models import Transactions
from .schemas import ChildrenReport
from .schemas import TransactionCreate
from .schemas import TransactionGetQuery
from .schemas import Report
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

    def get_transactions(self, transactions_get_query: TransactionGetQuery = Depends(...)
                         ) -> Optional[List[Transactions]]:
        return self._get_transactions(transactions_get_query)

    def get_report(self, transactions_get_query: TransactionGetQuery):
        transactions = self._get_transactions(transactions_get_query)
        time_points = set()
        operations = {'buy': ReportHierarchy('Покупка'), 'sale': ReportHierarchy('Продажа')}
        for row in transactions:
            row_type = row.type
            row_date = row.date
            time_points.add(row_date)
            row_amount = float(row.amount) * float(row.price)
            path = [
                row.shop_id,
                row.category_id,
                row.name,
            ]
            operations[row_type].add_child_elem(path, row_amount)
        print(operations)
        return Report(
            time_points=time_points,
            buy=self._add_child(operations['buy']),
            sale=self._add_child(operations['sale'])
        )

    def _get_transactions(self, transactions_get_query: TransactionGetQuery = Depends(...)
                          ) -> Optional[List[Transactions]]:
        transactions = self.session.execute(select(Transactions)
            .where(
            Transactions.category_id.in_(transactions_get_query.category)
            if transactions_get_query.category is not None else True,
            Transactions.shop_id.in_(transactions_get_query.category)
            if transactions_get_query.shop is not None else True,
            Transactions.date >= transactions_get_query.date_from
            if transactions_get_query.date_from is not None else True,
            Transactions.date <= transactions_get_query.date_to
            if transactions_get_query.date_to is not None else True,
        )).scalars().all()
        return transactions

    def _add_child(self, operations):
        return [ChildrenReport(
            name=str(row.name),
            amounts=row.amounts,
            total_amount=row.total_amount,
            children=self._add_child(row)
        ) for row in operations.children.values() if operations.children.values() is not None]


class ReportHierarchy:
    def __init__(self, name):
        self.name = name
        self.amounts = []
        self.total_amount = 0
        self.children = {}

    def add_child_elem(self, hierarchy, amount):
        self.amounts.append(amount)
        self.total_amount += amount

        if hierarchy:
            name = hierarchy.pop(0)
            try:
                child = self.children[name]
            except KeyError:
                child = self.children[name] = ReportHierarchy(name)
            child.add_child_elem(hierarchy, amount)
