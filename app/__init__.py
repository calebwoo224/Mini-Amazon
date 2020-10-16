from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging

#from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
#migrate = Migrate(app, db)
logging.basicConfig(filename="mini_amazon.log", filemode='w', level=logging.DEBUG)

from app import routes, models