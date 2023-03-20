from typing import List
from datetime import date

from sqlalchemy import ForeignKey, String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tablesoccer_rocks.extensions import db


class Player(db.Model):
    __tablename__ = "player"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(60), unique=True)
    last_name: Mapped[str] = mapped_column(String(30))
    first_name: Mapped[str] = mapped_column(String(30))

    dyp_histories_rel: Mapped[List["PlayerHistory"]] = relationship(back_populates="player")

    def __repr__(self) -> str:
        return f"Player(id={self.id!r}, last_name={self.last_name!r}, first_name={self.first_name!r})"


class PlayerHistory(db.Model):
    __tablename__ = "player_history"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    points: Mapped[int] = mapped_column(Integer)
    tendency: Mapped[int] = mapped_column(Integer, nullable=True)
    first: Mapped[int] = mapped_column(Integer, nullable=True)
    second: Mapped[int] = mapped_column(Integer, nullable=True)
    third: Mapped[int] = mapped_column(Integer, nullable=True)
    fourth: Mapped[int] = mapped_column(Integer, nullable=True)

    player_id = mapped_column(ForeignKey("player.id"))
    player: Mapped[Player] = relationship(back_populates="dyp_histories_rel")

    dyps_rel: Mapped[List["Dyp"]] = relationship(back_populates="player_history")

    def __repr__(self) -> str:
        return f"PlayerHistory(id={self.id!r}, place={self.place!r} points={self.points!r})"


class Dyp(db.Model):
    __tablename__ = "dyp"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    round: Mapped[int] = mapped_column(Integer)
    match_day: Mapped[int] = mapped_column(Integer)
    dyp_date: Mapped[date] = mapped_column(Date)

    player_history_id = mapped_column(ForeignKey("player_history.id"))
    player_history: Mapped[PlayerHistory] = relationship(back_populates="dyps_rel")

    def __repr__(self) -> str:
        return f"Dyp(id={self.id!r}, round={self.round!r}, match_day={self.match_day!r})"
