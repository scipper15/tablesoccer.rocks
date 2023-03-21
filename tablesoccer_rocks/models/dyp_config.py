from datetime import date

from sqlalchemy import CheckConstraint, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column

from tablesoccer_rocks.extensions import db


class DypConfig(db.Model):
    __tablename__ = "dyp_config"
    __table_args__ = (
        (CheckConstraint('id == 1')),
        {'extend_existing': True},
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    current_dyp_series: Mapped[int] = mapped_column(Integer)
    total_match_days: Mapped[int] = mapped_column(Integer)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    last_import_date: Mapped[date] = mapped_column(Date)
    last_import_match_day: Mapped[int] = mapped_column(Integer)
    first_points: Mapped[int] = mapped_column(Integer)
    second_points: Mapped[int] = mapped_column(Integer)
    third_points: Mapped[int] = mapped_column(Integer)
    fourth_points: Mapped[int] = mapped_column(Integer)
    participation_points: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"DypConfig(id={self.id!r}, \
            current_dyp_series={self.current_dyp_series!r} \
                last_import_date={self.last_import_date!r} \
                    last_import_match_day={self.last_import_match_day!r})"
