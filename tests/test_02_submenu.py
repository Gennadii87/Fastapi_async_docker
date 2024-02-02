from http import HTTPStatus
from typing import Any
from service import get_routes
from httpx import AsyncClient
from service import reverse


async def test_post_menu(
    menu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Добавление нового меню."""
    routes = get_routes()
    response = await client.post(
        reverse("create_menu", routes=routes),
        json=menu_post,)
    assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert 'submenus_count' in response.json(), 'Количества подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'

    saved_data['menu'] = response.json()


async def test_submenu_empty(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Проверка получения пустого списка подменю."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.get(
        reverse("read_all_submenus", menu_id=menu['id'],    routes=routes),)
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_post_submenu(
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Добавление нового подменю."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.post(
        reverse("create_submenu", menu_id=menu['id'], routes=routes),
        json=submenu_post,)
    assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора подменю нет в ответе'
    assert 'title' in response.json(), 'Названия подменю нет в ответе'
    assert 'description' in response.json(), 'Описания подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == submenu_post['title'], 'Название подменю не соответствует ожидаемому'
    assert response.json()['description'] == submenu_post['description'], 'Описание подменю не соответствует ожидаемому'

    saved_data['submenu'] = response.json()


async def test_post_submenu_same(
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Добавление нового подменю с одинаковым названием."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.post(
        reverse("create_submenu", menu_id=menu['id'], routes=routes),
        json=submenu_post,)
    assert response.status_code == HTTPStatus.BAD_REQUEST, 'Статус ответа не 400'


async def test_all_submenu_not_empty(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Проверка получения непустого списка подменю."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.get(
        reverse("read_all_submenus", menu_id=menu['id'], routes=routes),)
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() != [], 'В ответе пустой список'


async def test_get_posted_submenu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Получение созданного подменю."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse("read_submenu", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes),)
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == submenu['id'], 'Идентификатор подменю не соответствует ожидаемому'
    assert response.json()['title'] == submenu['title'], 'Название подменю не соответствует ожидаемому'
    assert response.json()['description'] == submenu['description'], 'Описание подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 0, 'Количество блюд не соответствует ожидаемому'


async def test_patch_submenu(
    submenu_patch: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Изменение текущего меню."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.patch(
        reverse("update_submenu", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes),
        json=submenu_patch,)
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert 'id' in response.json(), 'Идентификатора подменю нет в ответе'
    assert 'title' in response.json(), 'Названия подменю нет в ответе'
    assert 'description' in response.json(), 'Описания подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == submenu_patch['title'], 'Название подменю не соответствует ожидаемому'
    assert response.json()['description'] == submenu_patch['description'], \
        'Описание подменю не соответствует ожидаемому'

    saved_data['submenu'] = response.json()


async def test_get_patched_submenu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Получение обновленного подменю."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse("read_submenu", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == submenu['id'], 'Идентификатор подменю не соответствует ожидаемому'
    assert response.json()['title'] == submenu['title'], 'Название подменю не соответствует ожидаемому'
    assert response.json()['description'] == submenu['description'], 'Описание подменю не соответствует ожидаемому'
    assert response.json()['dishes_count'] == 0, 'Количество блюд не соответствует ожидаемому'


async def test_delete_submenu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Удаление текущего подменю."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.delete(
        reverse("delete_submenu", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == {"message": "Submenu deleted successfully"}, \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_submenu_empty_after_delete(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Проверка получения пустого списка подменю после удаления."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.get(
        reverse("read_all_submenus", menu_id=menu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_get_deleted_submenu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Получение удаленного подменю."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse("read_submenu", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, 'Статус ответа не 404'
    assert response.json()['detail'] == 'submenu not found', 'Сообщение об ошибке не соответствует ожидаемому'


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


async def test_deleted_menu_submenu_empty(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Проверка получения пустого списка подменю у несуществующего меню."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.get(
        reverse("read_all_submenus", menu_id=menu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_post_objects_for_cascade_check(
    menu_post: dict[str, str],
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Добавление нового меню и подменю для последующей проверки
    каскадного удаления."""
    routes = get_routes()
    response = await client.post(
        reverse("create_menu", routes=routes),
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'

    saved_data['menu'] = response.json()

    menu = saved_data['menu']
    response = await client.post(
        reverse("create_submenu", menu_id=menu['id'], routes=routes),
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'

    saved_data['submenu'] = response.json()


async def test_delete_cascade_menu(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Удаление меню."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.delete(
        reverse("delete_menu", menu_id=menu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == {"message": "Menu deleted successfully"}, \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_get_delete_cascade_menu_check(
    saved_data: dict[str, Any],
    client: AsyncClient,
) -> None:
    """Получение подменю удаленного меню."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse("read_submenu", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, 'Статус ответа не 404'
    assert response.json()['detail'] == 'submenu not found', \
        'Сообщение об ошибке не соответствует ожидаемому'
