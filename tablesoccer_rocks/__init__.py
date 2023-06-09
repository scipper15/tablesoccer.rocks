from flask import Flask
from flask_login import login_manager

from config import Config
from tablesoccer_rocks.extensions import db, login_manager
from tablesoccer_rocks.models.user import User
from tablesoccer_rocks.blueprints.main import bp as main_bp
from tablesoccer_rocks.blueprints.auth import bp as auth_bp
from tablesoccer_rocks.blueprints.admin import bp as admin_bp
from tablesoccer_rocks.blueprints.dyp import bp as dyp_bp
from tablesoccer_rocks.jinja_filters import format_date
from commands import init_db_bp, create_user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize extensions here
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u"Bitte einloggen um die Profilseite aufzurufen oder DYP-Ergebnisse einzutragen!"

    # register jinja template filters here
    admin_bp.app_template_filter(name=format_date)

    # register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dyp_bp)
    # command line commands
    app.register_blueprint(init_db_bp)
    app.register_blueprint(create_user_bp)

    # to test if development server works
    @app.route('/test/')
    def hello_world():
        return '<p>Hello, World!</p>'

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
