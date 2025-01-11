from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '695a4c8ec0498e2dfd972fa8cf8f31a00a0a0e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskblog.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


app.app_context().push()

from flaskblog import routes