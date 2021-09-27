from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from ..database import Base


class Accounts(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
