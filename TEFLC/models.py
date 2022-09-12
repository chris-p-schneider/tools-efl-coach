# models.py
# Data models for TEFLC
# --------------------------------------------

# Imports
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON

# My Files
from TEFLC import db, login_manager #app
# from __init__ import db, login_manager #test

# --------------------------------------------

# User Loader
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# --------------------------------------------

# Data Classes
class User(db.Model, UserMixin):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	imageFile = db.Column(db.String(20), nullable=False, default="default.png")
	password = db.Column(db.String(60), nullable=False)
	account = db.Column(JSON, nullable=False)
	# joined, verified, premium: date
	preferences = db.Column(JSON) # !:: add later
	# listViewDefault, autoSelectWord, safeMode...
	wordlists = db.relationship("WordList", backref="author", lazy=True)
	connected = db.Column(db.Integer, nullable=False, default=0) # !::
	
	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.imageFile}')"

class WordList(db.Model):
	__tablename__ = "wordlist"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	text = db.Column(db.Text, nullable=False)
	wordIds = db.relationship("WordBank", secondary="wordsAndLists", backref="lists", lazy="select")
	userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

	def __repr__(self):
		return f"WordList('{self.id}', '{self.title}', '{self.text}')"

class WordBank(db.Model):
	__tablename__ = "wordbank"
	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(128), nullable=False)
	wordInfo = db.Column(JSON, nullable=False)
	partsOfSpeech = db.Column(JSON) # !::
	# type: wordId
	
	def __repr__(self):
		return f"Word('{self.word}')"

# --------------------------------------------
# Relationship Tables
wordsAndLists = db.Table("wordsAndLists",
	db.Column("wordId", db.Integer, db.ForeignKey("wordbank.id"), nullable=False),
	db.Column("listId", db.Integer, db.ForeignKey("wordlist.id"), nullable=False)
	)