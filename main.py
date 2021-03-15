import base64
import random
import re
import os
from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/dashboard')
def dashboard():
    if hasattr(current_user, 'username'):
        if current_user.username == "crowadmin":
            return render_template('dashboard.html')
        else:
            return render_template('unauthorized.html')
    else:
        return render_template('unauthorized.html')


@main.route('/crows3/robots.txt')
def robots():
    return render_template('robots.html')


@main.route('/crows3/cr0w-s3cr3t')
def secret():
    return render_template('crows/crows-secret.html', level="Crows3")


@main.route('/crows5/cookie-source')
def cookie_source():
    return render_template('crows/crows5_viewsource.html', level="Crows5")


@main.route('/crows6/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        if request.form.get('secret') == "ReverseEngineering":
            return render_template('crows/crows6success.html', level='Crows6')
        else:
            return redirect(url_for(f'main.crows', i=6, msg=10))


@main.route('/crows6/viewsource')
def viewsource():
    return render_template('crows/crows6_viewsource.html', level="Crows6")


@main.route('/crows7/submit', methods=['POST'])
def crows7submit():
    if request.method == 'POST':
        if request.form.get('needle') != "":
            results = os.system(f"grep -i {request.form.get('needle')} /tmp/words.txt")
            return render_template('crows/crows7.html', level='Crows7', results=results)


@main.route('/crows7/viewsource')
def crows7viewsource():
    return render_template('crows/crows7_viewsource.html', level="Crows7")


@main.route('/crows<i>')
@login_required
def crows(i=""):
    # Handle crows3
    if 'robots.txt' in request.url and 'crows3' in request.url:
        return redirect(url_for('main.robots'))

    # Handle Crows4
    if request.headers.get('Referer') == "https://crowsctf.cf/crows5":
        return render_template(f'crows/crows4success.html', level=f'Crows4')

    # # Handle Crows5
    if 'crows5' in request.url and 'isAuthenticated' in request.cookies:
        if base64.b64decode(request.cookies['isAuthenticated']).decode('utf-8') == "True":
            return render_template('crows/crows5success.html', level='Crows5')

    msg = request.args.get('msg')
    if msg is None:
        msg = "0"

    msg = re.sub("[^\d]+", '', msg)

    if int(i) in range(0, 9):
        level = i
    else:
        level = 0

    if isinstance(msg, str):
        if msg == "":
            msg = 0
        if int(msg) == 0:
            flash(f"CAAWW!! You successfully logged in at Crows{i}, good luck.")
            return redirect(url_for(f'main.crows', i=i, msg=1))
        elif int(msg) == 10:
            flash(f'Wrong secret :( Keep trying!')
        else:
            random_message = [
                "Did you really think crows would hide hints like this?",
                "You do know that us crows can hold grudges right?",
                "Crow Gang CAW-CAW ",
                "HINT: No hints are hidden here.",
                "CAA'CAAAWWW!!!",
                "GIVE ME BREAD AND SHINY THINGS!",
                "Why do you keep refreshing this page?",
                "Those white crows are far inferior than us black crows.",
                "The funeral for lil Jimmy the Crow has been cancelled due to heavy storms.",
            ]

            flash(random_message[random.randint(0, 8)])

    return render_template(f'crows/crows{level}.html', level=f'Crows{level}')


if __name__ == "__main__":
    create_app().run(host='0.0.0.0')
