from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '695a4c8ec0498e2dfd972fa8cf8f31a00a0a0e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskblog.db'
db = SQLAlchemy(app)
app.app_context().push()

from flaskblog import routes