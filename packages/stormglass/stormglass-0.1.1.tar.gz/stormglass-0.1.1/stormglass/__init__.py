__version__ = "0.1.1"

__client = None


def resource(name: str, config: dict = None):
    from .client import __Client
    from .resources import get_resource

    global __client

    if not config:
        config = {}

    if not __client:
        __client = __Client(api_key=config.pop("api_key", None))

    return get_resource(name, client=__client)
