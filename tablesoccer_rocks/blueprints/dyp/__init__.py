from flask import Blueprint

bp = Blueprint('dyp', __name__)

from tablesoccer_rocks.blueprints.dyp import routes
