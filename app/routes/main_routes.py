from os import getenv
from flask import (
    Blueprint,
    current_app
)

from app.core import APIException


main = Blueprint('main', __name__)

@main.route('/')
def _main_route():
    raise APIException('Welcome to the Flask-Template!', status_code=200)

@main.route(getenv('ROUTE_ADMIN_DATAVIEW') or '/admin-dataview')
def _dataview():
    if current_app.config['DEBUG']:
        n = '_is_debug_mode_generate_dataview'
        if not hasattr(current_app, n):
            from app.admin import generate_dataview
            setattr(current_app, n, generate_dataview)

        _generate_dataview = getattr(current_app, n)
        
        return _generate_dataview()
    url_prefix = main.url_prefix or ''
    raise APIException(f'ERROR (Not Found): \'{url_prefix}/admin\'', status_code=404)

# 
@main.route('/<path:path>')
def _catch_all(path): 
    url_prefix = main.url_prefix or ''
    raise APIException(f'ERROR (Not Found): \'{url_prefix}/{path}\'', status_code=404)