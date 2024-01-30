from fastapi import APIRouter, Depends, HTTPException, status
from app.database.database import get_db
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.models import Dish as DBDish
from app.database.schemas import Dish, DishCreate
from app.config import prefixes, DISHES_LINK, DISH_LINK

router = APIRouter(prefix=prefixes)


@router.get(DISHES_LINK, response_model=List[Dish])
async def read_all_dishes(submenu_id: str, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBDish).filter(DBDish.submenu_id == submenu_id).offset(skip).limit(limit))
    db_dishes = result.scalars().all()
    return db_dishes


@router.get(DISH_LINK, response_model=Dish)
async def read_dish(submenu_id: str, dish_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBDish).filter(DBDish.id == dish_id, DBDish.submenu_id == submenu_id))
    db_dish = result.scalars().first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@router.post(DISHES_LINK, response_model=Dish, status_code=status.HTTP_201_CREATED)
async def create_dish(submenu_id: str, dish: DishCreate, db: AsyncSession = Depends(get_db)):
    async with db:
        db_dish = DBDish(**dish.dict(), submenu_id=submenu_id)
        db.add(db_dish)
        await db.commit()
        await db.refresh(db_dish)
        return db_dish


@router.patch(DISH_LINK, response_model=Dish)
async def update_dish(submenu_id: str, dish_id: str, dish: DishCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBDish).filter(DBDish.id == dish_id, DBDish.submenu_id == submenu_id))
    db_dish = result.scalars().first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    for key, value in dish.dict().items():
        setattr(db_dish, key, value)
    await db.commit()
    await db.refresh(db_dish)
    return db_dish


@router.delete(DISH_LINK)
async def delete_dish(submenu_id: str, dish_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBDish).filter(DBDish.id == dish_id, DBDish.submenu_id == submenu_id))
    db_dish = result.scalars().first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    await db.delete(db_dish)
    await db.commit()
    return {"message": "Dish deleted successfully"}
