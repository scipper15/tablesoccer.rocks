# Tablesoccer.rocks Project

## About The Project

Holds several scripts and web applications focused on table soccer:

- Web application with `xml`-import of `Draw Your Partner` tournaments held using [Kickertool]([Kickertool](https://kickertool.de/)).
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
6. Install `npm` dependencies:
   1. `cd .\tablesoccer_rocks\static\`
   2. `npm install`
7. Initialize database (go back to root folder):
   1. `flask --app tablesoccer_rocks shell`
   2. `>>> from init_db import init_db`
   3. `>>> init_db()`: This creates a `SQLite` database using models in `models`-folder.
8. Spin up development server: `flask --app tablesoccer_rocks run --debug`
9. Access page at `http://127.0.0.1:5000/`

## Usage

By default, a user `info@mitkickzentrale.de` is created. Password for development is `1234`.

This behavior can be changed in `init_db.py`. As of today this project is still built up. Many features are not yet implemented but may be added in future releases.

Sign-up feature is not yet implemented. You would access the database and insert a new user there (or delete the old one). Use `SHA256`-hashes for password hashing.

### How it works

`/dyp/` will redirect to the most recent match day and shows the rankings. To upload results you must login at `login`. You'll be redirected to `profile`. Update values here if necessary. A new menu entry is displayed if logged in: `Ergebnisse hochladen`.

At `upload_results` you choose a date and a `zip` file for the match day exported from [KickerTool](https://kickertool.de/). After hitting `import` a few things happen:

1. The file is uploaded to the server. Files with the same file name can't be uploaded twice to avoid duplicate imports.
2. The upload date is stored. The calendar is set to accept upload dates equal or greater than the last upload date.
3. The app extracts player names and rankings from the `xml` and writes the data to the database.
4. Match days are counted up automatically with each upload.
5. You'll be redirected showing the most recent ranking.

**N.b.:** After reaching maximum match days or the end date of the series (can be altered on the profile page), the database will be reset (!!) with the next file upload! This behavior will change in the future, but it was the easiest way to set up things smoothly, as old results aren't needed, as soon a new `D.Y.P.` series starts.

If a match day didn't take place you have to alter `Letzter Spieltag` in `profile` accordingly.

## License

## Contact

<reinhard.eichhorn@gmail.com>
