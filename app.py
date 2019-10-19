from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://pythonAPI:apisarecool@localhost:8889/pythonAPI'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'This_is_a_very_secret_key'

db = SQLAlchemy(app)