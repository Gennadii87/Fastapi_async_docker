from http import HTTPStatus
from typing import Any
from service import get_routes
from httpx import AsyncClient
from service import reverse
from decimal import Decimal


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
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора меню нет в ответе'
    assert 'title' in response.json(), 'Названия меню нет в ответе'
    assert 'description' in response.json(), 'Описания меню нет в ответе'
    assert 'submenus_count' in response.json(), 'Количества подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'

    saved_data['menu'] = response.json()


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
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора подменю нет в ответе'
    assert 'title' in response.json(), 'Названия подменю нет в ответе'
    assert 'description' in response.json(), 'Описания подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['title'] == submenu_post['title'], 'Название подменю не соответствует ожидаемому'
    assert response.json()['description'] == submenu_post['description'], 'Описание подменю не соответствует ожидаемому'

    saved_data['submenu'] = response.json()


async def test_dishes_empty(
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Проверка получения пустого списка блюд."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse("read_all_dishes", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_post_dish(
        dish_post: dict[str, str],
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Добавление нового блюда."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.post(
        reverse("create_dish", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes),
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора блюда нет в ответе'
    assert 'title' in response.json(), 'Названия блюда нет в ответе'
    assert 'description' in response.json(), 'Описания блюда нет в ответе'
    assert 'price' in response.json(), 'Цены блюда нет в ответе'
    assert response.json()['title'] == dish_post['title'], 'Название блюда не соответствует ожидаемому'
    assert response.json()['description'] == dish_post['description'], 'Описание блюда не соответствует ожидаемому'
    assert response.json()['price'] == str(Decimal(
        dish_post['price']).quantize(Decimal('0.00'))), 'Цена блюда не соответствует ожидаемой'

    saved_data['dish'] = response.json()


async def test_dish_read_create(
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Получение конкретного блюда."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse("read_dish", menu_id=menu['id'], submenu_id=submenu['id'],
                dish_id=dish['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == dish['id'], 'Идентификатор блюда не соответствует ожидаемому'
    assert response.json()['title'] == dish['title'], 'Название блюда не соответствует ожидаемому'
    assert response.json()['description'] == dish['description'], 'Описание блюда не соответствует ожидаемому'
    assert response.json()['price'] == dish['price'], 'Цена блюда не соответствует ожидаемой'


async def test_post_dish_same(
        dish_post: dict[str, str],
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Добавление нового блюда с одинаковым названием."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.post(
        reverse("create_dish", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes),
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST, 'Статус ответа не 400'


async def test_dish_not_empty(
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Проверка получения непустого списка блюд."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.get(
        reverse("read_all_dishes", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() != [], 'В ответе пустой список'


async def test_get_posted_dish(
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Получение созданного блюда."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse("read_dish", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes,
                dish_id=dish['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == dish['id'], 'Идентификатор блюда не соответствует ожидаемому'
    assert response.json()['title'] == dish['title'], 'Название блюда не соответствует ожидаемому'
    assert response.json()['description'] == dish['description'], 'Описание блюда не соответствует ожидаемому'
    assert response.json()['price'] == dish['price'], 'Цена блюда не соответствует ожидаемой'


async def test_patch_dish(
        dish_patch: dict[str, str],
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Изменение текущего блюда."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.patch(
        reverse("update_dish", menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id'], routes=routes),
        json=dish_patch,
    )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert 'id' in response.json(), 'Идентификатора блюда нет в ответе'
    assert 'title' in response.json(), 'Названия блюда нет в ответе'
    assert 'description' in response.json(), 'Описания блюда нет в ответе'
    assert 'price' in response.json(), 'Цены блюда нет в ответе'
    assert response.json()['title'] == dish_patch['title'], 'Название блюда не соответствует ожидаемому'
    assert response.json()['description'] == dish_patch['description'], 'Описание блюда не соответствует ожидаемому'
    assert response.json()['price'] == str(Decimal(
        dish_patch['price']).quantize(Decimal('0.00'))), 'Цена блюда не соответствует ожидаемой'

    saved_data['dish'] = response.json()


async def test_get_patched_dish(
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Получение созданного блюда."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse("read_dish", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes,
                dish_id=dish['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json()['id'] == dish['id'], 'Идентификатор блюда не соответствует ожидаемому'
    assert response.json()['title'] == dish['title'], 'Название блюда не соответствует ожидаемому'
    assert response.json()['description'] == dish['description'], 'Описание блюда не соответствует ожидаемому'
    assert response.json()['price'] == dish['price'], 'Цена блюда не соответствует ожидаемой'


async def test_delete_dish(
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Удаление текущего блюда."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.delete(
        reverse("delete_dish", menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == {"message": "Dish deleted successfully"}, \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_get_deleted_dish(
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Получение удаленного блюда."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await client.get(
        reverse("read_dish", menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, 'Статус ответа не 404'
    assert response.json()['detail'] == 'dish not found', 'Сообщение об ошибке не соответствует ожидаемому'


async def test_delete_submenu(
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Удаление текущего подменю."""
    routes = get_routes()
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await client.delete(
        reverse("delete_submenu", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes), )
    assert response.status_code == HTTPStatus.OK, \
        'Статус ответа не 200'
    assert response.json() == {"message": "Submenu deleted successfully"}, \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_delete_menu(
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Удаление текущего меню."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.delete(
        reverse("delete_menu", menu_id=menu['id'], routes=routes), )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == {"message": "Menu deleted successfully"}, \
        'Сообщение об удалении не соответствует ожидаемому'


async def test_all_menu_empty(client: AsyncClient) -> None:
    """Проверка получения пустого списка меню."""
    routes = get_routes()  # Получаем словарь маршрутов
    response = await client.get(
        reverse("read_all_menus", routes=routes),
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_post_objects_for_cascade(
        menu_post: dict[str, str],
        submenu_post: dict[str, str],
        dish_post: dict[str, str],
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Добавление нового меню подменю и блюда для проверки каскадного удаления."""
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

    submenu = saved_data['submenu']
    response = await client.post(
        reverse("create_dish", menu_id=menu['id'], submenu_id=submenu['id'], routes=routes),
        json=dish_post, )
    assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'

    saved_data['dish'] = response.json()


async def test_delete_menu_for_cascade(
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


async def test_get_deleted_menu_for_cascade(
        saved_data: dict[str, Any],
        client: AsyncClient,
) -> None:
    """Получение удаленного меню."""
    routes = get_routes()
    menu = saved_data['menu']
    response = await client.get(
        reverse("read_menu", menu_id=menu['id'], routes=routes),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND, \
        'Статус ответа не 404'
    assert response.json()['detail'] == 'menu not found', \
        'Сообщение об ошибке не соответствует ожидаемому'


async def test_all_menu_empty_for_cascade(client: AsyncClient) -> None:
    """Проверка получения пустого списка меню."""
    routes = get_routes()  # Получаем словарь маршрутов
    response = await client.get(
        reverse("read_all_menus", routes=routes),  # Передаем словарь маршрутов вместе с endpoint_name
    )
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'
