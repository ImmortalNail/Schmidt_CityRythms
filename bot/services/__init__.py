from .base import start, age_verification, get_name
from .registration import get_age
from .routes import show_routes, route_selected, confirm_participation
from .photos import handle_photo

__all__ = [
    'start',
    'age_verification',
    'get_name',
    'get_age',
    'show_routes',
    'route_selected',
    'confirm_participation',
    'handle_photo'
]