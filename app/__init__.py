import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


from app.server_config import ServerConfig

# Flask app
app = Flask(__name__)
app.config.from_object(ServerConfig)
'''
refer to - https://itnext.io/how-and-why-have-a-properly-configuration-handling-file-using-flask-1fd925c88f4c
change above line to:
app.config.from_envvar('CONFIGURATION_FILE')
$ export CONFIGURATION_FILE=./config/debug_environment.cfg
'''

# Database setup
db = SQLAlchemy(app)
bcrypt = Bcrypt()

from app.user.routes import user
app.register_blueprint(user, url_prefix='/api/user')

from app.stocks.routes import stocks
app.register_blueprint(stocks, url_prefix='/api/stocks')

print(app.url_map)