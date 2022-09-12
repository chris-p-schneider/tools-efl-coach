# __init__.py
# Converts TEFLC.py into a package.
# --------------------------------------------

# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
import random

# My Files
from TEFLC.getWordInfo.getWordImgs import getWordImgs
from TEFLC.wordInfo import getWordInfo, getListInfo

# --------------------------------------------

SECRET_KEY = "very_secret" # example for github
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
moment = Moment(app)
bootstrap = Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = "loginPage"
# login_manager.login_message_category = "className"

# --------------------------------------------
# GLOBAL FUNCTIONS
def shuffleList(userList):
	shuffledList = userList.copy()
	random.shuffle(shuffledList)
	return shuffledList

def getImages(word):
	wordImgs = getWordImgs(word)
	return wordImgs

# ADD FUNCTIONS TO JINJA ENV
app.jinja_env.globals.update(getImages=getImages)
app.jinja_env.globals.update(shuffleList=shuffleList)

# --------------------------------------------

# Import after defining db
from TEFLC import routes #app

# --------------------------------------------