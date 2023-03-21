from datetime import datetime

from flask import redirect, url_for, render_template, request, flash
from flask_login import login_required

from tablesoccer_rocks.extensions import db
from tablesoccer_rocks.blueprints.admin import bp
from tablesoccer_rocks.models.dyp_config import DypConfig
from init_db import init_dyp_config


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # n.b. DypConfig is meant to hold only one row of data
    dyp_config = db.session.get(DypConfig, 1)

    if not dyp_config:
        # create (initialize) first and only record after login
        dyp_config = init_dyp_config()
    if request.method == 'POST':
        # get column names of table
        column_names = DypConfig.__table__.columns.keys()
        # remove some as we won't need them in subsequent loop
        del column_names[0]  # remove key 'id'
        del column_names[4]  # remove last_date_updated
        del column_names[4]  # remove last_match_day_updated
        # check if all fields are filled
        errors = False
        for name in column_names:
            if request.form.get(name, 0) == 0:
                errors = True
                flash(f'Bitte Feld {name} ausfüllen.')
        if errors:
            return redirect(url_for('views.admin.profile', _anchor='errors'))

        # save form data to database
        dyp_config.current_dyp_series = request.form['current_dyp_series']
        dyp_config.total_match_days = request.form['total_match_days']
        dyp_config.start_date = datetime.strptime(request.form['start_date'], '%d.%m.%Y')
        dyp_config.end_date = datetime.strptime(request.form['end_date'], '%d.%m.%Y')
        dyp_config.first_points = request.form['first_points']
        dyp_config.second_points = request.form['second_points']
        dyp_config.third_points = request.form['third_points']
        dyp_config.fourth_points = request.form['fourth_points']
        dyp_config.participation_points = request.form['participation_points']
        db.session.commit()
        # re-read the updates for display
        dyp_config = db.session.get(DypConfig, 1)
    print(dyp_config)

    return render_template(
        'admin/profile.html',
        dyp_config=dyp_config
    )
