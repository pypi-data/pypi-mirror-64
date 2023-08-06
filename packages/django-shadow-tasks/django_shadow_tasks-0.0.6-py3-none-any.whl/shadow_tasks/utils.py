import pika

__all__ = (
    'get_broker_connection',
    'get_func_full_path',
)


def get_broker_connection():
    from shadow_tasks.settings import shadow_settings

    conn_params = pika.URLParameters(shadow_settings.BROKER_URL)
    return pika.BlockingConnection(conn_params)


def get_func_full_path(func):
    return f'{func.__module__}.{func.__name__}'
