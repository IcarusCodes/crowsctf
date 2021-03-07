from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

accepted_users = ['Crows0', 'Crows1', 'Crows2', 'Crows3', 'Crows4', 'Crows5', 'Crows6']


@auth.route('/login')
def login():
    if request.method == 'GET':
        stage = request.args.get('stage')
        if stage is not None:
            if int(stage) not in range(0, 8):
                stage = 0
        else:
            stage = 0
    return render_template('login.html', stage=stage)


@auth.route('/login', methods=['POST', 'GET'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user:
        if user.username.lower() == "crowadmin" and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))

    if not user or not check_password_hash(user.password, password):
        flash(f'Invalid username or password.')
        return redirect(url_for(f'auth.login'))

    if user.username.lower() not in [f'crows{x}' for x in range(0, 8)]:
        flash(f'Only Crows users allowed.')
        return redirect(url_for(f'auth.login', stage=stage))

    login_user(user)

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
