from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from models import Dish, Menu, SubMenu


async def check_menu_exists(db: AsyncSession, menu_id: str) -> None:
    """Проверка на существование меню."""
    query = select(exists().where(Menu.id == menu_id))
    exists_menu = await db.scalar(query)
    if not exists_menu:
        raise NoResultFound('Menu not found')


async def check_submenu_exists(db: AsyncSession, submenu_id: str) -> None:
    """Проверка на существование подменю."""
    query = select(exists().where(SubMenu.id == submenu_id))
    exists_submenu = await db.scalar(query)
    if not exists_submenu:
        raise NoResultFound('Submenu not found')


async def check_dish_exists(db: AsyncSession, dish_id: str) -> None:
    """Проверка на существование блюда."""
    query = select(exists().where(Dish.id == dish_id))
    exists_dish = await db.scalar(query)
    if not exists_dish:
        raise NoResultFound('Dish not found')
