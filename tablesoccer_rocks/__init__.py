from flask import Flask
from tablesoccer_rocks.extensions import db

from config import Config
from tablesoccer_rocks.blueprints.main import bp as frontend_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize extensions here
    db.init_app(app)

    # register blueprints here
    app.register_blueprint(frontend_bp)

    # for testing if development server works
    @app.route('/test/')
    def hello_world():
        return '<p>Hello, World!</p>'

    return app
