"""Usage:
- Start app in development mode: `flask --app tablesoccer_rocks run --debug`
- Initialize database: `flask --app tablesoccer_rocks shell`, then: `import init_db`

drop_all() in flask shell will delete all tables defined in models.py.
To create a new secret key: `python -c 'import secrets; print(secrets.token_hex())'`.
Will be loaded from a `.env`-file not included in repository.
"""

import os
from pathlib import Path
from sys import platform
import secrets

from dotenv import load_dotenv

if Path.is_file(Path('.env')):
    pass
else:
    with open('.env', 'w') as file:
        key = secrets.token_hex()
        file.write(f"SECRET_KEY='{key}'")

load_dotenv()

class Config:
    BASE_DIR = Path(__file__).parent.resolve()
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_NAME = 'dyp.sqlite'

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    UPLOAD_FOLDER = 'dyp_results'
    XML_QUALIFYING_FILE_NAME = 'qualifying-group-1.xml'
    XML_ELIMINATION_FILE_NAME = 'elimination-KO-Baum 1.xml'
    ALLOWED_EXTENSIONS = {'zip'}

    Path.mkdir(BASE_DIR / UPLOAD_FOLDER, exist_ok=True)
