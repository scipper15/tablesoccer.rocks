from datetime import date
from tablesoccer_rocks.blueprints.admin.routes import bp


@bp.app_template_filter('format_date')
def format_date(my_date: date) -> str:
    return my_date.strftime('%d.%m.%Y')
