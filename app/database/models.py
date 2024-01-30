import uuid
from sqlalchemy import Column, String, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, index=True)
    description = Column(String)
    submenus = relationship("SubMenu", back_populates="menu", cascade="all, delete-orphan")


class SubMenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, index=True)
    description = Column(String)
    menu_id = Column(UUID, ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(DECIMAL(precision=10, scale=4))
    submenu_id = Column(UUID, ForeignKey("submenus.id"), index=True, nullable=False)
    submenu = relationship("SubMenu", back_populates="dishes")
