from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from ..config import get_settings
from ..database import get_session
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError
from .models import Categories
from .schemas import CategoryChange
from .models import Shops
from .schemas import ShopChange


class ShopService:
    def __init__(self, session=Depends(get_session), settings=Depends(get_settings)):
        self.session = session
        self.settings = settings

    def create_shop(self, shop_create: ShopChange) -> Shops:
        shop = Shops(name=shop_create.name)
        self.session.add(shop)
        try:
            self.session.commit()
            return shop
        except IntegrityError:
            raise EntityConflictError from None

    def create_category(self, category_create: CategoryChange) -> Categories:
        category = Categories(name=category_create.name)
        self.session.add(category)
        try:
            self.session.commit()
            return category
        except IntegrityError:
            raise EntityConflictError from None

    def update_shop(self, shop_id: int, shop_update: ShopChange) -> Shops:
        shop = self._get_shop(shop_id)
        if not shop_update.name:
            return shop
        shop.name = shop_update.name
        self.session.commit()
        return shop

    def update_category(self, category_id: int, category_update: ShopChange) -> Shops:
        category = self._get_category(category_id)
        if not category_update.name:
            return category
        category.name = category_update.name
        self.session.commit()
        return category

    def delete_shop_by_id(self, shop_id: int):
        try:
            shop = self.session.execute(
                select(Shops).where(Shops.id == shop_id)).scalar_one()
            self.session.delete(shop)
            self.session.commit()
            return shop
        except NoResultFound:
            raise EntityDoesNotExistError from None


    def delete_category_by_id(self, category_id: int):
        try:
            category = self.session.execute(
                select(Categories).where(Categories.id == category_id)).scalar_one()
            self.session.delete(category)
            self.session.commit()
            return category
        except NoResultFound:
            raise EntityDoesNotExistError from None

    def _get_shop(self, shop_id: int) -> Shops:
        try:
            shop = self.session.execute(
                select(Shops)
                .where(Shops.id == shop_id)
            ).scalar_one()
            return shop
        except NoResultFound:
            raise EntityDoesNotExistError from None

    def _get_category(self, category_id: int):
        try:
            category = self.session.execute(
                select(Categories)
                .where(Categories.id == category_id)
            ).scalar_one()
            return category
        except NoResultFound:
            raise EntityDoesNotExistError from None
