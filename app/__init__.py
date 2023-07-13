from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import db, User
from flask_moment import Moment
from .api import api

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api)

db.init_app(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
moment = Moment(app)

@login_manager.user_loader
def load_user(user_id):
    # return User.query.filter_by(id=user_id).first()
    return User.query.get(user_id)

login_manager.login_view = 'loginPage'

from . import routes, models