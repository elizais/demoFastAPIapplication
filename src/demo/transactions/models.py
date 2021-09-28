from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String

from ..database import Base


class Transactions(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    date = Column(String, nullable=False)
    shop_id = Column(ForeignKey('shops.id'), nullable=False)
    category_id = Column(ForeignKey('categories.id'))
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
