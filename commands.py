import re
from datetime import date
from pathlib import Path

import click
from flask import Blueprint
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from config import Config
from tablesoccer_rocks.extensions import db
from tablesoccer_rocks.models.user import User
from tablesoccer_rocks.models.dyp_config import DypConfig
from tablesoccer_rocks.models.dyp_models import Player, PlayerHistory, Dyp

create_user_bp = Blueprint('user', __name__)
init_db_bp = Blueprint('db', __name__)


@init_db_bp.cli.command('init')
def init_db():
    if Path.is_file(Path(Config.BASE_DIR) / Config.DB_NAME):
        print(f'Database <{Config.DB_NAME}> not initialized. Delete existing database first.')
    db.drop_all()
    db.create_all()
    print('Database created.')
    init_dyp_config()
    print('DypConfig initialized.')


@create_user_bp.cli.command('create')
@click.argument('user_name')
@click.argument('user_password')
def create_user(user_name, user_password):
    """Create new user: Provide user name and password as parameters.

    Args:
        user_name (str): user name
        user_password (str): user password
    """
    try:
        if password_check(user_password)['password_ok']:
          new_user = User(
              user_name=user_name,
              password_hash=generate_password_hash(user_password, method='sha256')
              )
          db.session.add(new_user)
          db.session.commit()
        else:
            for description, error in password_check(user_password).items():
                print(description, error)
            print('Password requirements not met. User not created.')
            return
    except:
        raise Exception('An Error ocurred. User not created.')
    print(f'Created new user: {user_name}')


def init_dyp_config():
    dyp_config = DypConfig(
        id=1,
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
        participation_points=10
    )
    db.session.add(dyp_config)
    db.session.commit()


def password_check(password):
    """
    Check strength of 'password'.
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"\W", password) is None
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

    return {
        'password_ok' : password_ok,
        'length_error' : length_error,
        'digit_error' : digit_error,
        'uppercase_error' : uppercase_error,
        'lowercase_error' : lowercase_error,
        'symbol_error' : symbol_error,
    }


if __name__ == '__main__':
    pass
