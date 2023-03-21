from flask import Blueprint

bp = Blueprint('admin', __name__)

from tablesoccer_rocks.blueprints.admin import routes
