import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

ENV = 'dev'
# ENV = 'prod'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://moringa:root@localhost/moringa'
    app.config['SECRET_KEY'] = '4963fe5782355fc76e4821f231207f5f14216e10'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pjdhspwenpzbge:0bb5f9b23f5ea9bffb769e0bf5eea1f1b84a777aa5a3e1178ce5e025def0bc6b@ec2-54-209-221-231.compute-1.amazonaws.com:5432/d1f4533kntv8i4'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes