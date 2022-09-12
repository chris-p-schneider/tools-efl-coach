# forms.py
# Form classes for TEFLC
# --------------------------------------------

# Imports
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, FieldList, FormField, Form
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user

# My Files 
from TEFLC.models import User

# --------------------------------------------
# User Registration
class RegistrationForm(FlaskForm):
	username = StringField("Username", 
				validators=[DataRequired(), 
				Length(min=3, max=20)])
	
	email = StringField("Email",
				validators=[DataRequired(), 
				Email()])

	password = PasswordField("Password",
				validators=[DataRequired()])

	confirmPassword = PasswordField("Confirm Password",
				validators=[DataRequired(), 
				EqualTo("password")])

	submit = SubmitField("Sign Up")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username is taken. Choose a new username.")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Email is taken. Use a new email.")

# --------------------------------------------
# User Login
class LoginForm(FlaskForm):
	email = StringField("Email",
				validators=[DataRequired(), 
				Email()])

	password = PasswordField("Password",
				validators=[DataRequired()])

	remember = BooleanField("Remember Me")

	submit = SubmitField("Log In")

# --------------------------------------------
# User Account Info Update
class UpdateAccountForm(FlaskForm):
	username = StringField("Username", 
				validators=[DataRequired(), 
				Length(min=3, max=20)])
	
	email = StringField("Email",
				validators=[DataRequired(), 
				Email()])

	picture = FileField("Profile Picture",
				validators=[FileAllowed(["jpg", "jpeg", "png"])])

	submit = SubmitField("Update")

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("Username is taken. Choose a new username.")

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("Email is taken. Use a new email.")

# --------------------------------------------
# New List Input
class ListForm(FlaskForm):
	listTitle = StringField("List Title", 
				validators=[DataRequired()])
	text = TextAreaField("Word List", id="list-form-textarea", 
				validators=[DataRequired()])
	submit = SubmitField("Save")

# --------------------------------------------
# Image List: 3 default, max 9
class ImageList(Form):
	image1 = StringField("Image 1", 
				validators=[Length(max=224)])
	image2 = StringField("Image 2", 
				validators=[Length(max=224)])
	image3 = StringField("Image 3", 
				validators=[Length(max=224)])
	image4 = StringField("Image 4", 
				validators=[Length(max=224)])
	image5 = StringField("Image 5", 
				validators=[Length(max=224)])
	image6 = StringField("Image 6", 
				validators=[Length(max=224)])
	image7 = StringField("Image 7", 
				validators=[Length(max=224)])
	image8 = StringField("Image 8", 
				validators=[Length(max=224)])
	image9 = StringField("Image 9", 
				validators=[Length(max=224)])

# --------------------------------------------
# Word Verification - Basic
class WordVerificationBasic(FlaskForm):
	wordType = SelectField("Word Type", 
				id="word-verification-type",
				choices=[("adjective", "adjective"),
						("adverb", "adverb"),
						("conjunction", "conjunction"),
						("contraction", "contraction"),
						("determiner", "determiner"),
						("exclamation",  "exclamation"),
						("idiom", "idiom"),
						("interjection", "interjection"),
						("noun", "noun"),
						("preposition", "preposition"),
						("pronoun", "pronoun"),
						("verb", "verb"),
						("other", "[other]")],
				validators=[DataRequired()])
	wordDefinition = TextAreaField("Word Definition", 
					id="word-verification-definition",
					validators=[DataRequired()])
	wordImages = FormField(ImageList)
	wordImageSelected = StringField("Word Image", 
				id="word-verification-image-selected-url", 
				validators=[Length(max=224)])
	wordImageUpload = FileField("Image Upload",
				id="word-verification-image-upload",
				validators=[FileAllowed(["jpg", "jpeg", "png", "gif"])])
	submit = SubmitField("Submit Verification",
						id="word-verification-submit-button")

# --------------------------------------------
# Full Verification: Bottom Column
class BottomColumn(Form):
	word1 = StringField("Word 1", 
				validators=[Length(max=124)])
	word2 = StringField("Word 2", 
				validators=[Length(max=124)])
	word3 = StringField("Word 3", 
				validators=[Length(max=124)])
	word4 = StringField("Word 4", 
				validators=[Length(max=124)])
	word5 = StringField("Word 5", 
				validators=[Length(max=124)])
	word6 = StringField("Word 6", 
				validators=[Length(max=124)])
	word7 = StringField("Word 7", 
				validators=[Length(max=124)])
	word8 = StringField("Word 8", 
				validators=[Length(max=124)])
	word9 = StringField("Word 9", 
				validators=[Length(max=124)])
	word10 = StringField("Word 10", 
				validators=[Length(max=124)])

# --------------------------------------------
# Word Verification - Full
class WordVerificationFull(FlaskForm):
	wordType = SelectField("Word Type", 
				id="word-verification-type",
				choices=[("adjective", "adjective"),
						("adverb", "adverb"),
						("conjunction", "conjunction"),
						("contraction", "contraction"),
						("determiner", "determiner"),
						("exclamation",  "exclamation"),
						("idiom", "idiom"),
						("interjection", "interjection"),
						("noun", "noun"),
						("preposition", "preposition"),
						("pronoun", "pronoun"),
						("verb", "verb"),
						("other", "[other]")],
				validators=[DataRequired()])
	wordSyllables = IntegerField("Syllables", 
					id="word-verification-syllables", 
					validators=[NumberRange(min=1, max=12)])
	wordDefinition = TextAreaField("Word Definition", 
					id="word-verification-definition",
					validators=[DataRequired()])
	wordImages = FormField(ImageList)
	wordImageSelected = StringField("Word Image", 
				id="word-verification-image-selected-url", 
				validators=[Length(max=224)])
	# add later
	wordImageUpload = FileField("Image Upload",
				id="word-verification-image-upload",
				validators=[FileAllowed(["jpg", "jpeg", "png", "gif"])])
	wordSentence = TextAreaField("Sentence", 
					id="word-verification-sentence",
					validators=[DataRequired(),
						Length(max=224)])
	# Use string > textarea then loop one per entry
	wordRelated = FormField(BottomColumn)
	wordSynonyms = FormField(BottomColumn)
	wordAntonyms = FormField(BottomColumn)
	wordRhymes = FormField(BottomColumn)
	submit = SubmitField("Submit Verification",
						id="word-verification-submit-button")

# --------------------------------------------

# XY Form: Wordsearch
class XYInput (FlaskForm):
	xValue = IntegerField("X:", 
				id="x-value", 
				validators=[NumberRange(min=10, max=100)])
	yValue = IntegerField("Y:", 
				id="y-value", 
				validators=[NumberRange(min=10, max=100)])
	submit = SubmitField("Submit",
						id="xy-submit")

# --------------------------------------------