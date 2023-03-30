from pathlib import Path
from datetime import datetime, timedelta

from flask import redirect, url_for, render_template, request, flash
from flask_login import login_required
from werkzeug.utils import secure_filename

from config import Config
from tablesoccer_rocks.extensions import db
from tablesoccer_rocks.blueprints.admin import bp
from tablesoccer_rocks.models.dyp_config import DypConfig
from tablesoccer_rocks.blueprints.admin.utils import save_results_from_dyp2db, get_xml_from_zip, \
    get_players_from_dyp_xml


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
            return redirect(url_for('admin.profile', _anchor='errors'))

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

    return render_template(
        'admin/profile.html',
        dyp_config=dyp_config
    )


@bp.route('/upload_results', methods=['GET', 'POST'])
@login_required
def upload_results():
    if request.method == 'POST':
        # performing checks
        if not request.form['date-picker']:
            flash('Bitte Datum festlegen.')
            return redirect(request.url)
        dyp_date = datetime.strptime(request.form['date-picker'], '%d.%m.%Y')

        if 'uploaded-file' not in request.files:
            flash('Es kam kein file_part an.')
            return redirect(request.url)
        file = request.files['uploaded-file']

        if file.filename == '':
            flash('Keine Datei ausgewählt.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            if file_already_exists(file_name):
                flash(f'Diese Turnierergebnisse sind bereits hochgeladen worden: "{file_name}".')
                return render_template('admin/upload_results.html')

            # n.b.: save zip: to avoid double upload / import
            file.save(Path(Config.UPLOAD_FOLDER) / file_name)
            # extract data from xml
            qualifying_tree = get_xml_from_zip(file, file_name, Config.XML_QUALIFYING_FILE_NAME)
            elimination_tree = get_xml_from_zip(file, file_name, Config.XML_ELIMINATION_FILE_NAME)
            result_xml_qualifying = get_players_from_dyp_xml(qualifying_tree)
            result_xml_elimination = get_players_from_dyp_xml(elimination_tree)

            # finally write xml data to db
            save_results_from_dyp2db(result_xml_qualifying, result_xml_elimination, dyp_date)

            dyp_config = db.session.get(DypConfig, 1)

            return redirect(url_for(
                'dyp.show_results',
                match_day=dyp_config.last_import_match_day)
                )
        else:
            flash(f'Nicht erlaubter Dateityp: "{file.filename}". Bitte eine "zip"-Ergebnisdatei hochladen.')

    # for calendar: sets the min date selectable with date picker
    dyp_config = db.session.get(DypConfig, 1)
    last_import_date = dyp_config.last_import_date + timedelta(days=7)
    return render_template(
        'admin/upload_results.html',
        last_import_date=last_import_date
        )


def allowed_file(file_name):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def file_already_exists(file_name):
    return True if Path.is_file(Path(Config.UPLOAD_FOLDER) / file_name) else False
