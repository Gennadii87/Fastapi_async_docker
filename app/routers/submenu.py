from fastapi import APIRouter, Depends, HTTPException, status
from app.database.database import get_db
from typing import List, cast as typing_cast

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import prefixes, SUBMENUS_LINK, SUBMENU_LINK
from app.database.schemas import SubMenu, SubMenuCreate
from app.database.models import SubMenu as DBSubMenu, Dish as DBDish

router = APIRouter(prefix=prefixes)


@router.get(SUBMENUS_LINK, response_model=List[SubMenu])
async def read_all_submenus(menu_id: str, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    submenus = await db.execute(select(DBSubMenu, func.count(DBDish.id).label("dishes_count")).outerjoin(DBDish)
                                .filter(DBSubMenu.menu_id == menu_id).group_by(DBSubMenu.id).offset(skip).limit(limit))

    submenus_with_counts = [
        SubMenu(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,
            dishes_count=dishes_count
        )
        for submenu, dishes_count in submenus
    ]

    return submenus_with_counts


@router.get(SUBMENU_LINK, response_model=SubMenu)
async def read_submenu(menu_id: str, submenu_id: str, db: AsyncSession = Depends(get_db)):
    submenu = (await db.execute(select(DBSubMenu).filter(DBSubMenu.id == submenu_id, DBSubMenu.menu_id == menu_id))
               ).scalars().first()
    if submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    dishes_count = (await db.execute(select(func.count()).where(typing_cast(str, DBDish.submenu_id) == submenu.id))
                    ).scalar()

    submenu_with_counts = SubMenu(
        id=submenu.id,
        title=submenu.title,
        description=submenu.description,
        dishes_count=dishes_count
    )

    return submenu_with_counts


@router.post(SUBMENUS_LINK, response_model=SubMenu, status_code=status.HTTP_201_CREATED)
async def create_submenu(menu_id: str, submenu: SubMenuCreate, db: AsyncSession = Depends(get_db)):
    async with db:
        submenu_data = submenu.dict()
        submenu_data["menu_id"] = menu_id

        db_submenu = DBSubMenu(**submenu_data)
        db.add(db_submenu)
        await db.commit()
        await db.refresh(db_submenu)
        return db_submenu


@router.patch(SUBMENU_LINK, response_model=SubMenu)
async def update_submenu(menu_id: str, submenu_id: str, submenu: SubMenuCreate, db: AsyncSession = Depends(get_db)):
    db_submenu = (await db.execute(select(DBSubMenu).filter(DBSubMenu.id == submenu_id, DBSubMenu.menu_id == menu_id))
                  ).scalars().first()
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    for key, value in submenu.dict(exclude_unset=True).items():
        setattr(db_submenu, key, value)
    await db.commit()
    await db.refresh(db_submenu)
    return db_submenu


@router.delete(SUBMENU_LINK)
async def delete_submenu(menu_id: str, submenu_id: str, db: AsyncSession = Depends(get_db)):
    submenu = (await db.execute(select(DBSubMenu).filter(DBSubMenu.id == submenu_id, DBSubMenu.menu_id == menu_id))
               ).scalars().first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    await db.delete(submenu)
    await db.commit()
    return {f'message: Submenu deleted successfully'}
