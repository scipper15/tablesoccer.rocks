from datetime import datetime
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ElTree

from sqlalchemy import func, select, update
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert

from tablesoccer_rocks.extensions import db
from tablesoccer_rocks.models.dyp_config import DypConfig
from tablesoccer_rocks.models.dyp_models import Player, PlayerHistory, Dyp


def save_results_from_dyp2db(qualifying_tree, elimination_tree, dyp_date):
    update_dyp_config(dyp_date)
    dyp_config = db.session.get(DypConfig, 1)
    match_day = dyp_config.last_import_match_day

    for qualifying in qualifying_tree:
        full_name = qualifying['name']
        first_name, last_name = full_name.split(' ')

        points = dyp_config.participation_points
        first, second, third, fourth = False, False, False, False
        # plus points for the first 4 places
        for elimination in elimination_tree:
            if qualifying['name'] == elimination['name']:
                place = int(elimination['platz'])
                if place == 1:
                    points += dyp_config.first_points
                    first = True
                elif place == 2:
                    points += dyp_config.second_points
                    second = True
                elif place == 3:
                    points += dyp_config.third_points
                    third = True
                elif place == 4:
                    points += dyp_config.fourth_points
                    fourth = True

        stmt = sqlite_upsert(Player).values(
            full_name=full_name, last_name=last_name, first_name=first_name,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[Player.full_name], set_=dict(full_name=stmt.excluded.full_name)
        )
        db.session.execute(stmt)

        player = db.session.scalars(
            stmt.returning(Player), execution_options={"populate_existing": True}
        ).first()

        p = player
        dh = PlayerHistory(
            points=points,
            tendency=0,
            first=1 if first else 0,
            second=1 if second else 0,
            third=1 if third else 0,
            fourth=1 if fourth else 0,
        )
        d = Dyp(
            round=dyp_config.current_dyp_series,
            match_day=match_day,
            dyp_date=dyp_date,
        )

        db.session.add(p)
        db.session.add(dh)
        db.session.add(d)
        p.dyp_histories_rel.append(dh)
        dh.dyps_rel.append(d)

        db.session.commit()

    write_tendencies()


def write_tendencies():
    status = db.session.get(DypConfig, 1)
    if status.last_import_match_day <= 1:
        # all done: tendency has already been saved as 0
        return
    else:
        old_ranking = get_ranking_table_data(
            status.current_dyp_series,
            status.last_import_match_day - 1
        )
        new_ranking = get_ranking_table_data(
            status.current_dyp_series,
            status.last_import_match_day
        )
        for old_place, player_old in enumerate(old_ranking):
            for new_place, player_new in enumerate(new_ranking):
                if player_old.full_name == player_new.full_name:
                    if new_place == old_place:
                        new_tendency = 0
                    elif new_place < old_place:
                        new_tendency = 1  # player ranked up compared to last match day
                    else:
                        new_tendency = -1

                    stmt = update(PlayerHistory).where(
                        Player.id == PlayerHistory.player_id,
                        PlayerHistory.id == Dyp.player_history_id,
                        Player.full_name == player_new.full_name,
                        Dyp.round == status.current_dyp_series,
                        Dyp.match_day == status.last_import_match_day
                    ).values(
                        tendency=new_tendency
                    )
                    db.session.execute(stmt)
                    db.session.commit()


def update_dyp_config(dyp_date):
    # update last updated values
    dyp_config = db.session.get(DypConfig, 1)
    dyp_config.last_import_date = dyp_date

    # increment match days automatically
    # TODO IMPLEMENT: if the case, user should be advised on next login
    #  (message box if either of the two conditions is satisfied)
    if dyp_config.last_import_match_day <= dyp_config.total_match_days \
            or dyp_config.end_date_dyp_series <= datetime.now():
        dyp_config.last_import_match_day += 1
    else:
        dyp_config.last_import_match_day = 1
        dyp_config.current_dyp_series += 1
        drop_tables_for_new_season()

    db.session.commit()


def drop_tables_for_new_season():
    Dyp.__table__.drop(db.engine)
    PlayerHistory.__table__.drop(db.engine)
    Player.__table__.drop(db.engine)
    db.create_all()


def get_ranking_table_data(dyp_round, match_day):
    ranking = db.session.execute(
        select(
            Player.full_name,
            func.count(Player.full_name).label('participation_count'),
            PlayerHistory.tendency.label('current_tendency'),
            func.sum(PlayerHistory.points).label('points_total'),
            func.sum(PlayerHistory.first).label('first'),
            func.sum(PlayerHistory.second).label('second'),
            func.sum(PlayerHistory.third).label('third'),
            func.sum(PlayerHistory.fourth).label('fourth'),
        ).outerjoin(
            PlayerHistory
        ).join(
            Dyp
        ).filter(
            Dyp.round == dyp_round,
            Dyp.match_day <= match_day  # page id
        ).order_by(
            func.sum(PlayerHistory.points).desc(),
            # important!!! this will ensure that the most current value of tendency is selected
            # otherwise tendency won't show correctly / won't change
            func.row_number().over(func.max(PlayerHistory.id))
        ).group_by(
            Player.full_name
        )
    )
    return ranking.all()


def get_amount_jackpot(dyp_round, match_day):
    amount_jackpot = db.session.execute(
        select(
            func.count(Player.full_name).label('amount_jackpot'),
        ).outerjoin(
            PlayerHistory
        ).join(
            Dyp
        ).filter(
            Dyp.round == dyp_round,
            Dyp.match_day <= match_day  # page id
        )).scalar_one_or_none()
    return amount_jackpot


def build_table_data(ranking_table, ranking):
    ranking_table.append(
        {
            'full_name': ranking.full_name,
            'participation_count': ranking.participation,
            'total_points': ranking.points_total,
            'average_points': ranking.points_total / ranking.participation,
            'first_points': ranking.first,
            'second_points': ranking.second,
            'third_points': ranking.third,
            'fourth_points': ranking.fourth,
        }
    )
    return ranking_table


def get_xml_from_zip(file_obj, zip_file_name, xml_filename):
    with zipfile.ZipFile(file_obj, 'r') as zip_ref:
        in_zip_path = Path(zip_file_name).stem  # Path(file_name).stem equals path inside zip
        with zip_ref.open(rf'{in_zip_path}/{xml_filename}') as my_xml:
            return my_xml.read()


def get_players_from_dyp_xml(my_xml):
    results = []
    root_sport = ElTree.fromstring(my_xml)
    for child_disziplin in root_sport:
        for child_meldung in child_disziplin:
            results.append(child_meldung.attrib)
    return results
