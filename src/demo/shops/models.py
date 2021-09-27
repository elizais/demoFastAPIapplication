from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from ..database import Base


class Shops(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
