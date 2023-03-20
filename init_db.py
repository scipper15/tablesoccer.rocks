from werkzeug.security import generate_password_hash

from tablesoccer_rocks.extensions import db
from tablesoccer_rocks.models.user import User
from tablesoccer_rocks.models.dyp_models import Player, PlayerHistory, Dyp

db.drop_all()
db.create_all()

# create new default user for testing
if not db.session.get(User, 1):
    new_user = User(
        user_name='info@mitkickzentrale.de',
        password_hash=generate_password_hash('1234', method='sha256')
        )

    db.session.add(new_user)
    db.session.commit()
