from pydantic import BaseModel, UUID4, field_validator
from decimal import Decimal
from typing import Union


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class Menu(MenuBase):
    id: UUID4
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    pass


class SubMenu(SubMenuBase):
    id: UUID4
    title: str
    description: str
    dishes_count: int = 0


class DishBase(BaseModel):
    title: str
    description: str
    price: Decimal


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: UUID4
    title: str
    description: str
    price: Union[Decimal, str]

    @field_validator('price')
    def validate_price(cls, v: Decimal):
        return f'{v:.2f}'
