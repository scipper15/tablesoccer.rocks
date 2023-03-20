from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

from tablesoccer_rocks.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "player"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)


    def __repr__(self):
        return f'<User "{self.user_name}">'
