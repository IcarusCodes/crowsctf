import base64

from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from datetime import datetime

auth = Blueprint('auth', __name__)


@auth.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@auth.route('/login')
def login():
    if request.method == 'GET':
        stage = request.args.get('stage')
        if stage is not None:
            if int(stage) not in range(0, 9):
                stage = 0
        else:
            stage = 0
    return render_template('login.html', stage=stage)


@auth.route('/login', methods=['POST', 'GET'])
def login_post():
    stage = request.form.get('stage')

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user:
        if user.username.lower() == "crowadmin" and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))

    if not user or not check_password_hash(user.password, password):
        flash(f'Invalid username or password.')
        return redirect(url_for(f'auth.login', stage=stage))

    login_user(user)

    if stage == "5":
        resp = make_response(redirect(url_for('main.crows', i=user.username[-1], msg=0)))
        custom_cookie = base64.b64encode(b'Go to /crows5/cookie-source').decode('utf-8') + "=="
        resp.set_cookie("isAuthenticated", custom_cookie)
        return resp

    return redirect(url_for(f'main.crows', i=user.username[-1], msg=0))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user:
        flash("User already exists")
        return redirect(url_for('auth.signup'))

    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
