from http import HTTPStatus
from typing import Any
from service import get_routes
from httpx import AsyncClient
from service import reverse


async def test_all_menu_empty(client: AsyncClient) -> None:
    """Проверка получения пустого списка меню."""
    routes = get_routes()  # Получаем словарь маршрутов
    response = await client.get(
        reverse("read_all_menus", routes=routes),  # Передаем словарь маршрутов вместе с endpoint_name
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_post_menu(
    menu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Добавление нового меню."""
    routes = get_routes()
    response = await client.post(
        reverse("create_menu", routes=routes),
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert 'submenus_count' in response.json(), 'Количества подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == menu_post['title'], 'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == menu_post['description'], 'Описание меню не соответствует ожидаемому'

    saved_data['menu'] = response.json()


async def test_post_menu_double(
    menu_post: dict[str, str],
    client: AsyncClient,
) -> None:
    """Добавление нового меню с одинаковым названием."""
    routes = get_routes()
    response = await client.post(
        reverse("create_menu", routes=routes),
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST, 'Статус ответа не 400'


async def test_all_menu_not_empty(client: AsyncClient) -> None:
    """Проверка получения непустого списка меню."""
    routes = get_routes()
    response = await client.get(
        reverse("read_all_menus", routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() != [], 'В ответе пустой список'


async def test_get_posted_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Получение созданного меню."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.get(reverse("read_menu", menu_id=menu['id'], routes=routes))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == menu['id'], 'Идентификатор меню не соответствует ожидаемому'
    assert response.json()['title'] == menu['title'], 'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == menu['description'], 'Описание меню не соответствует ожидаемому'
    assert response.json()['submenus_count'] == 0, 'Количество подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 0, 'Количество блюд не соответствует ожидаемому'


async def test_patch_menu(
    menu_patch: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Изменение текущего меню."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.patch(
        reverse("update_menu", menu_id=menu['id'], routes=routes),
        json=menu_patch,
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert 'submenus_count' in response.json(), 'Количества подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == menu_patch['title'], 'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == menu_patch['description'], 'Описание меню не соответствует ожидаемому'

    saved_data['menu'] = response.json()


async def test_get_patched_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Получение обновленного меню."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.get(
        reverse("read_menu", menu_id=menu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == menu['id'], 'Идентификатор меню не соответствует ожидаемому'
    assert response.json()['title'] == menu['title'], 'Название меню не соответствует ожидаемому'
    assert response.json()['description'] == menu['description'], 'Описание меню не соответствует ожидаемому'
    assert response.json()['submenus_count'] == 0, 'Количество подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 0, 'Количество блюд не соответствует ожидаемому'


async def test_delete_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Удаление текущего меню."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.delete(
        reverse("delete_menu", menu_id=menu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == {"message": "Menu deleted successfully"}, \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_get_deleted_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Получение удаленного меню."""
    routes=get_routes()
    menu = saved_data['menu']
    response = await client.get(
        reverse("read_menu", menu_id=menu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, 'Статус ответа не 404'
    assert response.json()['detail'] == 'menu not found', 'Сообщение об ошибке не соответствует ожидаемому'
