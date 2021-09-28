from collections import Counter
from datetime import date
from typing import Dict
from typing import ForwardRef
from typing import List
from typing import Optional


from pydantic import BaseModel


class Transaction(BaseModel):
    id: int
    type: str = ['buy', 'sale']
    date: str
    shop_id: int
    category_id: Optional[int]
    name: str
    price: float
    amount: float

    class Config:
        orm_mode = True


class TransactionCreate(BaseModel):
    type: str = ['buy', 'sale']
    date: str
    shop_id: int
    category_id: Optional[int]
    name: str
    price: float
    amount: float


class TransactionGetQuery(BaseModel):
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    shop: Optional[List[int]] = None
    category: Optional[List[int]] = None


class ChildrenReport(BaseModel):
    name: str
    amounts: List[float]
    total_amount: float
    children: List['ChildrenReport'] = None


ChildrenReport.update_forward_refs()


class Report(BaseModel):
    time_points: list[str]
    buy: List[ChildrenReport]
    sale: List[ChildrenReport]
