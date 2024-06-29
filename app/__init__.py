import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = os.urandom(24)
# app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:152189@localhost/stock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 指定登录视图的端点
login_manager.login_message_category = 'info'

from app import routes, models
