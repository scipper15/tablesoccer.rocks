from flask import Blueprint

bp = Blueprint('auth', __name__)

from tablesoccer_rocks.blueprints.auth import routes
