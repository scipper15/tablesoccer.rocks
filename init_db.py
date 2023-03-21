from datetime import date

from werkzeug.security import generate_password_hash

from tablesoccer_rocks.extensions import db
from tablesoccer_rocks.models.user import User
from tablesoccer_rocks.models.dyp_config import DypConfig
from tablesoccer_rocks.models.dyp_models import Player, PlayerHistory, Dyp


def init_db():
    db.drop_all()
    db.create_all()
    create_test_user()
    init_dyp_config()


def create_test_user():
    if not db.session.get(User, 1):
        new_user = User(
            user_name='info@mitkickzentrale.de',
            password_hash=generate_password_hash('1234', method='sha256')
            )
        db.session.add(new_user)
        db.session.commit()


def init_dyp_config():
    dyp_config = DypConfig(
        id = 1,
        current_dyp_series=30,
        total_match_days=25,
        start_date=date(2022, 11, 10),
        end_date=date(2023, 5, 11),
        last_import_date=date(2022, 11, 10),
        last_import_match_day=0,
        first_points=20,
        second_points=15,
        third_points=10,
        fourth_points=5,
        participation_points = 10
    )
    db.session.add(dyp_config)
    db.session.commit()

if __name__ == '__main__':
    init_db()
