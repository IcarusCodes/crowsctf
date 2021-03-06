import random, re

from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from . import db
from datetime import datetime

main = Blueprint('main', __name__)


@main.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@main.route('/')
def index():
    return render_template('index.html')


# @main.route('/static/crows2/files')
# def files():
#     # return "<h1> UGH </h1>"
#     return send_from_directory("users.txt", "/static/crows2/files")


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/crows<i>')
@login_required
def crows(i=""):
    msg = request.args.get('msg')
    if msg is None:
        msg = "0"

    msg = re.sub("[^\d]+", '', msg)

    if int(i) in range(0, 8):
        level = i
    else:
        level = 0

    if isinstance(msg, str):
        if msg == "":
            msg = 0
        if int(msg) == 0:
            flash(f"CAAWW!! You successfully logged in at Crows{i}, good luck.", )
            return redirect(url_for(f'main.crows', i=i, msg=1))
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

    return render_template(f'crows/crows{level}.html', level=f'Crows{i}')


if __name__ == "__main__":
    create_app().run(host='0.0.0.0')
