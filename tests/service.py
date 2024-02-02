from app.main import app


def get_routes() -> dict[str, str]:
    """Получение словаря с маршрутами приложения."""
    routes = {}
    for route in app.routes:
        routes[route.endpoint.__name__] = route.path
    return routes


def reverse(endpoint_name: str, routes: dict[str, str], **kwargs) -> str:
    """Получение url адреса."""
    path = routes.get(endpoint_name)
    if path is None:
        raise ValueError(f"Endpoint '{endpoint_name}' not found in routes.")
    return path.format(**kwargs)