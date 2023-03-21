from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user

from tablesoccer_rocks.models.user import User
from tablesoccer_rocks.blueprints.auth import bp


@bp.route('/login')
def login():
    return render_template('auth/login.html')


@bp.route('/login', methods=('GET', 'POST'))
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(user_name=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password_hash, password):
        flash('Passwort oder Benutzername falsch. Versuche es bitte noch einmal.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('admin.profile'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('auth/logout.html')
