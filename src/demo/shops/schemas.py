from typing import Optional

from pydantic import BaseModel


class Shop(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ShopChange(BaseModel):
    name: str


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CategoryChange(BaseModel):
    name: str



