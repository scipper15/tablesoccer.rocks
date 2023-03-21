# Tablesoccer.rocks Project

## About The Project

Holds several scripts and web applications focused on table soccer:

- Web application with XML-import of `Draw Your Partner` tournaments held using [Kickertool]([Kickertool](https://kickertool.de/)).
- Todo: Import player data via web scraping from [Bayerischer Tischfußball Verband e.V.](https://btfv.de/) pages.
- Todo: Web application calculating and showing player ratings over time using [TrueSkill](https://en.wikipedia.org/wiki/TrueSkill), based on previously scraped data.

Used by [Mitkickzentrale](https://mitkickzentrale.de/), a registered, self-governed, non-profit organization dedicated to promoting table soccer.

## Built With

- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
  - [Flask-SQLAlchemy](https://flask-sqlalchemypalletsprojects.com/en/3.0.x/)
  - [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- [Jinja](https://jinja.palletsprojects.com/en/3.1.x/)
- [SQLite](https://sqlite.org/index.html)
- [SQLalchemy](https://www.sqlalchemy.org/)
- [Bulma](https://bulma.io/)
- [jQuery](https://jquery.com/)
- [Font Awesome](https://fontawesome.com/)
- [npm](https://www.npmjs.com/)

### Prerequisites

- `Python 3.9+`.

### Installation

1. Clone from `GitHub`: `git clone https://github.com/scipper15/tablesoccer.rocks.git`.
2. `cd tablesoccer.rocks`
3. Create virtual environment: `python -m venv ./.venv --upgrade-deps`
4. Activate environment: `.\.venv\Scripts\activate`
5. Install requirements: `pip install -r requirements.txt`.
6. Install `np dependencies:
   1. `cd .\tablesoccer_rocks\static\`
   2. `npm install`
7. Initialize database (go back to root folder):
   1. `flask --app tablesoccer_rocks shell`
   2. `>>> from init_db import init_db`
   3. `>>> init_db()`: This creates a `SQLite` database using models in `models`-folder.
8. Spin up development server: `flask --app tablesoccer_rocks run --debug`
9. Access page on `http://127.0.0.1:5000/`

## Usage

By default, a user `info@mitkickzentrale.de` is created. Password for development is `1234`. This behavior can be changed in `init_db.py`. As of today this project is still built up. Many features are not yet implemented but may be added in future releases.

## License

## Contact

[Martin-Reinhard Eichhorn](reinhard.eichhorn@gmail.com)
