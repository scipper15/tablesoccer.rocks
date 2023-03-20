from flask import render_template

from tablesoccer_rocks.blueprints.main import bp


@bp.route('/')
def index():
    return render_template('main/index.html')
