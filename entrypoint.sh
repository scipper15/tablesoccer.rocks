#!/bin/bash
echo "Initializing database:"
flask db init
echo "Creating user:"
# length >= 8, plus min. 1 symbol, 1 upper and lower case, 1 number
flask user create new_user new_passworD1@

echo "Creating virtual environment"
python3 -m venv .venv_linux
. .venv_linux/bin/activate
echo "Installing dependencies from requirements.txt"
pip install -r requirements.txt

echo "Altering owner and permissions"
chown www-data:www-data -R
find . -type d -exec chmod 755 {} \;  # folders
find . -type d -exec chmod 644 {} \;  # files

echo "Starting server for deployment with 4 workers on standard port 8000"
gunicorn -w 4 'tablesoccer_rocks:create_app()'
