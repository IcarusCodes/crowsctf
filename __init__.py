from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mobility import Mobility

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    Mobility(app)

    app.config['SECRET_KEY'] = "what3v3r"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('notfound.html'), 404

    # blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    def has_access(user, stage):
        if user in [f'Crows{x}' for x in range(stage, 8)]:
            return True
        else:
            return False
    app.jinja_env.globals.update(has_access=has_access)

    return app
