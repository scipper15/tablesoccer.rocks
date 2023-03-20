from flask import Blueprint

bp = Blueprint('main', __name__)

from tablesoccer_rocks.blueprints.main import routes
