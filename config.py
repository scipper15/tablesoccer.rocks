"""Usage:
- Start app in development mode: `flask --app tablesoccer_rocks run --debug`
- Initialize database: `flask --app tablesoccer_rocks shell`, then: `import init_db`

drop_all() in flask shell will delete all tables defined in models.py.
To create a new secret key: `python -c 'import secrets; print(secrets.token_hex())'`.
Will be loaded from a `.env`-file not included in repository.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_DIR = Path(__file__).parent.resolve()
    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'dyp.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
