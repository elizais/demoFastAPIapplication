from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from .schemas import Category
from .schemas import CategoryChange
from .schemas import Shop
from .schemas import ShopChange
from .services import ShopService
from ..auth.services import get_current_account
from ..auth.schemas import AuthAccount
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError

router = APIRouter(
    prefix=''
)


@router.post(
    '/shops',
    response_model=Shop,
    status_code=status.HTTP_201_CREATED,
)
def create_shop(
        shop_create: ShopChange,
        current_account: AuthAccount = Depends(get_current_account),
        service: ShopService = Depends()
):
    try:
        shop = service.create_shop(shop_create)
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT) from None
    return shop


@router.post(
    '/category',
    response_model=Category,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
        category_create: CategoryChange,
        current_account: AuthAccount = Depends(get_current_account),
        service: ShopService = Depends()
):
    try:
        category = service.create_category(category_create)
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT) from None
    return category


@router.put('/shops/{shop_id}', response_model=Shop)
def update_shop(
    shop_id: int,
    shop_update: ShopChange,
    current_account: AuthAccount = Depends(get_current_account),
    service: ShopService = Depends(),
):
    try:
        shop = service.update_shop(shop_id, shop_update)
        return shop
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.put('/category/{category_id}', response_model=Shop)
def update_category(
    category_id: int,
    category_update: ShopChange,
    current_account: AuthAccount = Depends(get_current_account),
    service: ShopService = Depends(),
):
    try:
        category = service.update_shop(category_id, category_update)
        return category
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.delete('/category/{category_id}', response_model=Category)
def delete_category(
    category_id: int,
    current_account: AuthAccount = Depends(get_current_account),
    service: ShopService = Depends(),
):
    try:
        category = service.delete_category_by_id(category_id)
        return category
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None
