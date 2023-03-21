from flask import render_template, redirect, url_for
from tablesoccer_rocks.extensions import db

from tablesoccer_rocks.models.dyp_config import DypConfig
from tablesoccer_rocks.blueprints.dyp import bp
from tablesoccer_rocks.blueprints.admin.utils import get_amount_jackpot, get_ranking_table_data

@bp.route('/dyp/spieltag/<int:match_day>')
@bp.route('/dyp/spieltag/')
@bp.route('/dyp/')
def show_results(match_day=None):
    dyp_config = db.session.get(DypConfig, 1)
    if match_day is None or match_day > dyp_config.last_import_match_day:
        return redirect(url_for('dyp.show_results', match_day=dyp_config.last_import_match_day))
    elif match_day == 0 and dyp_config.last_import_match_day > 0:
        return redirect(url_for('dyp.show_results', match_day=dyp_config.last_import_match_day))

    ranking_data = get_ranking_table_data(dyp_config.current_dyp_series, match_day)
    total_match_days = list(range(1, dyp_config.last_import_match_day + 1))
    # remove match day which is being displayed from dropdown in template
    del total_match_days[match_day - 1]
    dyp_info = {
        'match_day': match_day,
        'total_match_days': total_match_days,
        'amount_jackpot': get_amount_jackpot(dyp_config.current_dyp_series, match_day)
    }

    return render_template(
        'dyp/show_results.html',
        current_ranking=ranking_data,
        dyp_config=dyp_config,
        dyp_info=dyp_info
    )
