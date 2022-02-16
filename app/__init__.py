import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

ENV = 'prod'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://moringa:root@localhost/moringa'
    app.config['SECRET_KEY'] = '4963fe5782355fc76e4821f231207f5f14216e10'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sdogvgcnwlalft:64d928e3490fc7d4aacb691dc86c6820fe0174ec684a043777d031c1e0cb5e93@ec2-54-83-21-198.compute-1.amazonaws.com:5432/d4kvqed26qnl7p'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes