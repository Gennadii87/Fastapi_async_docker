import os

from dotenv import load_dotenv

load_dotenv()
prefixes = '/api/v1'
# PREFIX_LINK = 'http://127.0.0.1:8000/api/v1'
MENUS_LINK = '/menus/'
MENU_LINK = '/menus/{menu_id}'
SUBMENUS_LINK = '/menus/{menu_id}/submenus/'
SUBMENU_LINK = '/menus/{menu_id}/submenus/{submenu_id}'
DISHES_LINK = '/menus/{menu_id}/submenus/{submenu_id}/dishes/'
DISH_LINK = '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST=os.getenv('POSTGRES_HOST')

conn_url = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
