# routes.py
# Routes for TEFLC.py
# --------------------------------------------

# Imports
import os, re, redis
import os.path, json, datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta
import random
from redis import Redis
from rq import Queue
import secrets, time, threading
from PIL import Image
from flask import render_template
from flask import url_for, request
from flask import redirect, flash, abort, Response
from flask_login import login_user, current_user, logout_user, login_required

# My Files
from TEFLC import app, db, bcrypt, moment, bootstrap
from TEFLC.forms import RegistrationForm, LoginForm, UpdateAccountForm, ListForm, WordVerificationBasic, WordVerificationFull, XYInput
from TEFLC.models import User, WordList, WordBank
from TEFLC.wordInfo import getWordInfo, getListInfo
from TEFLC.static.py.wordsearch import generateWordSearch
# --------------------------------------------

# Landing page from Teachers.EFL.Coach
@app.route ("/")
def landingPage ():
	connectedList = 0
	if current_user.is_active:
		if current_user.connected != 0:
			connectedList = WordList.query.filter_by(id=current_user.connected).first()
			if not connectedList:
				connectedList = current_user.wordlists[-1]
				current_user.connected = connectedList.id
				db.session.commit()
	return render_template("landing.html",
							connectedList=connectedList)

# --------------------------------------------

# User Registration Page
@app.route("/register", methods=["GET", "POST"])
def registrationPage ():
	if current_user.is_authenticated:
		return redirect(url_for("accountPage"))
	form = RegistrationForm()
	if form.validate_on_submit():
		newAccount = {
			"joined": str(datetime.datetime.now().isoformat()),
			"verified": "",
			"premium": ""
		}
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user = User(username=form.username.data, email=form.email.data, password=hashed_password,
					account=newAccount)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created for {form.username.data}! You can now log in.', "alert-success")
		return redirect(url_for("loginPage"))
	return render_template("account/register.html",
							title="Register", 
							form=form)

# User Login Page
@app.route("/login", methods=["GET", "POST"])
def loginPage ():
	if current_user.is_authenticated:
		return redirect(url_for("accountPage"))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get("next")
			flash(f"Welcome back, " + str(user.username) + "!", "alert-success")
			return redirect (next_page) if next_page else redirect(url_for("landingPage"))
		else: 
			flash("Oops! That wasn't right.", "alert-fail")
	return render_template("account/login.html",
							title="Log In", 
							form=form)

@app.route("/logout", methods=["GET", "POST"])
def logoutPage ():
	logout_user()
	return redirect(url_for("landingPage"))

# --------------------------------------------

def savePicture(formPicture):
	randomHex = secrets.token_hex(8)
	_, fExt, = os.path.splitext(formPicture.filename)
	pictureFilename = randomHex + fExt
	picturePath = os.path.join(app.root_path, "static/img/profile-pics", pictureFilename)
	output_size = (200, 200)
	i = Image.open(formPicture)
	i.thumbnail(output_size)
	i.save(picturePath)
	return pictureFilename

# User Account page
# Landing > Account
# Lists [New, Edit, Clone, Combine]
@app.route("/account", methods=["GET", "POST"])
@login_required
def accountPage ():
	# Update Account
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			pictureFile = savePicture(form.picture.data)
			current_user.imageFile = pictureFile
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Your account has been updated.", "alert-success")
		return redirect (url_for("accountPage"))
	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
	imageFile = url_for("static", filename="img/profile-pics/" + current_user.imageFile)
	return render_template("account/account.html",
							title="My Account",
							imageFile=imageFile,
							form=form)

# Upgrade Account
# need payment app, etc
@app.route("/upgrade")
@login_required
def upgradePage ():
	joinDate = dateutil.parser.parse(current_user.account["joined"])
	memberFor = relativedelta(datetime.datetime.now(), joinDate)
	return render_template("account/upgrade.html",
							title="Upgrade",
							memberFor=memberFor)

# --------------------------------------------
# LISTS
# --------------------------------------------

# Global List Variables to pass between newListPage and listLoadingPage
cleanText = ""
newListTitle = "" 

# New Vocab List
@app.route("/new-list", methods=["GET", "POST"])
@login_required
def newListPage ():
	form = ListForm()
	if form.validate_on_submit():
		# clean text to space delimiter
		dirtyText = form.text.data
		if re.findall(",+", dirtyText): 
			cleanText = "\n".join([w for w in dirtyText.split(", ") if len(w)>1])
		elif re.findall("	+", dirtyText):
			cleanText = "\n".join([w for w in dirtyText.split("	") if len(w)>1])
		elif re.findall("\n+", dirtyText):
			cleanText = "\n".join([w for w in dirtyText.split("\n") if len(w)>1])
		else:
			cleanText = "\n".join([w for w in dirtyText.split() if len(w)>1])
		regex = re.compile("[^a-zA-Z '!?\.\n-]")
		cleanText = regex.sub("", cleanText)
		cleanText = "\n".join([w for w in cleanText.split("\n") if len(w)>1])
		cleanText = re.sub("i'", "I'", cleanText)

		cleanList = cleanText.split('\n')
		
		# Check if words in db, add to db if not
		for word in cleanList:
			existingWord = WordBank.query.filter_by(word=word).first()
			if existingWord: 
				pass
			else:
				newEntry = WordBank(word=word,
					wordInfo = getWordInfo(word))
				db.session.add(newEntry)
				db.session.commit()
		
		# Commit to db
		newList = WordList(title=form.listTitle.data,
					text=cleanText,
					author=current_user)
		db.session.add(newList)
		db.session.commit()
		
		# Add relationships
		for word in cleanList:
			existingWord = WordBank.query.filter_by(word=word).first()
			newList.wordIds.append(existingWord)
			db.session.commit()

		flash("Your list has been saved!", "alert-success")
		return redirect(url_for("accountPage"))

	'''
	else:
		flash("Something went wrong.", "alert-fail")
		return redirect(url_for("accountPage"))
	'''						
	return render_template("list/newList.html",
							title="New List",
							form=form,
							legend="New List")

# Create list as background process
'''
@app.route("/create-list", methods=["GET", "POST"])
@login_required

# Queue
# redis = redis.Redis()
'''

# Display Progress of List Getting Info
'''
@app.route("/loading", methods=["GET", "POST"])
@login_required
def listLoadingPage ():
	
	word = "test"
	progress = 10
	seconds = 70

	return render_template ("list/listLoading.html",
							title="Loading...",
							word=word,
							progress=progress,
							seconds=seconds)
'''

# Unique User List
@app.route("/list/<int:listId>", methods=["GET", "POST"])
@login_required
def listPage (listId):
	wordList = WordList.query.get_or_404(listId)
	# ordListIds = wordList.wordIds
	'''
	wordIdInfo = {} # dict of wordId : wordInfo
	# can use wordInfo.word to get word
	for wordId in wordListIds:
		wordUsed = WordBank.query.filter_by(id=wordListIds[wordId]).first()
		wordIdInfo[wordListIds[wordId]] = wordUsed.wordInfo
	'''
	return render_template ("list/list.html",
							title=wordList.title,
							wordList=wordList)

# Update User List
@app.route("/list/<int:listId>/edit", methods=["GET", "POST"])
@login_required
def listEditPage (listId):
	wordList = WordList.query.get_or_404(listId)
	if wordList.author != current_user:
		abort(403)
		# return redirect (url_for("cloneList"))
	form = ListForm()
	if form.validate_on_submit():
		wordList.title = form.listTitle.data
		wordList.text = form.text.data
		db.session.commit()
		flash("Your list has been edited successfully.", "alert-success")
		return redirect(url_for("listPage", listId=wordList.id))
	elif request.method == "GET":
		form.listTitle.data = wordList.title
		form.text.data = wordList.text

	return render_template ("list/newList.html",
							title="Edit List",
							wordList=wordList,
							form=form,
							legend="Edit List")

# Connect User List
@app.route("/list/<int:listId>/connect", methods=["GET", "POST"])
@login_required
def listConnectPage (listId):
	wordList = WordList.query.get_or_404(listId)
	current_user.connected = listId
	db.session.commit()
	flash("Your list has been connected!", "alert-success")
	return redirect(url_for("landingPage"))

# Delete User List
@app.route("/list/<int:listId>/delete", methods=["POST"])
@login_required
def listDeletePage (listId):
	wordList = WordList.query.get_or_404(listId)
	if wordList.author != current_user:
		abort(403)
	db.session.delete(wordList)
	db.session.commit()
	flash("Your list has been deleted.", "alert-fail")
	return redirect(url_for("accountPage"))

# List Info Page
@app.route("/list-info")
def listInfoPage():
	return render_template ("list/listInfo.html",
						title="List Info")

# --------------------------------------------
# WORDS
# --------------------------------------------

# Unique Word
@app.route("/word/<int:wordId>", methods=["GET", "POST"])
@login_required
def wordPage (wordId):
	word = WordBank.query.get_or_404(wordId)
	return render_template ("word/word.html",
							title=word.word,
							word=word,
							wordId=word.id)

# Verify Word: Basic
@app.route("/word/<int:wordId>/verify/basic", methods=["GET", "POST"])
@login_required
def basicWordVerificationPage (wordId):
	form = WordVerificationBasic()
	word = WordBank.query.get_or_404(wordId)
	if form.validate_on_submit():
		# Copy Original
		wordInfoCopy = word.wordInfo.copy()
		
		# Update the Copy
		wordInfoCopy.update({"wordV": 1})
		wordInfoCopy.update({"type": form.wordType.data})
		wordInfoCopy.update({"typeV": word.wordInfo["typeV"]+1})
		wordInfoCopy.update({"definition": form.wordDefinition.data})
		wordInfoCopy.update({"definitionV": word.wordInfo["definitionV"]+1})
		# Word Images
		wordImagesTemp = []
		for value in form.wordImages.data:
			if form.wordImages.data[value] != "":
				wordImagesTemp.append(form.wordImages.data[value])
		wordImagesTemp = list(dict.fromkeys(wordImagesTemp))
		wordImagesTemp.sort()
		wordInfoCopy.update({"images": wordImagesTemp})
		wordInfoCopy.update({"imagesV": word.wordInfo["imagesV"]+1})
		wordInfoCopy.update({"imageSelected": form.wordImageSelected.data})

		# Update JSON Column
		word.wordInfo = wordInfoCopy
		db.session.commit()
		
		# Save as JSON to Words Directory
		projectDir = "/home/chsch/Documents/PYTHON/Tools.EFL.Coach/TEFLC v0.0.1/TEFLC"
		wordsDir = "/data/words/updated/"

		wordJSON = json.dumps(wordInfoCopy, indent=4, ensure_ascii=False)
		with open (projectDir + wordsDir + str(word.wordInfo["word"])+".json", "w") as f:
			f.write(wordJSON)
			f.close()

		flash("Basic info for \"" + word.wordInfo["word"] + "\" verified successfully.", "alert-success")
		return redirect(url_for("wordPage", wordId=wordId))


	return render_template ("word/wordVerificationBasic.html",
							title=word.word,
							word=word,
							wordId=word.id,
							form=form)

# Update Full Word: Verification Full & Word Edit
# Input word & form, output updated dict
def updateWordCopy(word, form, intWordV):
		wordInfoCopy = word.wordInfo.copy()
		
		# Update the Copy
		wordInfoCopy.update({"wordV": intWordV})
		wordInfoCopy.update({"type": form.wordType.data})
		wordInfoCopy.update({"typeV": word.wordInfo["typeV"]+1})
		wordInfoCopy.update({"definition": form.wordDefinition.data})
		wordInfoCopy.update({"definitionV": word.wordInfo["definitionV"]+1})
		# Word Images
		wordImagesTemp = []
		for value in form.wordImages.data:
			if form.wordImages.data[value] != "":
				wordImagesTemp.append(form.wordImages.data[value])
		wordImagesTemp = list(dict.fromkeys(wordImagesTemp))
		wordImagesTemp.sort()
		wordInfoCopy.update({"images": wordImagesTemp})
		wordInfoCopy.update({"imagesV": word.wordInfo["imagesV"]+1})
		wordInfoCopy.update({"imageSelected": form.wordImageSelected.data})
		# Syllables & Sentence
		wordInfoCopy.update({"syllables": form.wordSyllables.data})
		wordInfoCopy.update({"syllablesV": word.wordInfo["syllablesV"]+1})
		wordInfoCopy.update({"sentence": form.wordSentence.data})
		wordInfoCopy.update({"sentenceV": word.wordInfo["sentenceV"]+1})
		# Related Words
		wordRelatedTemp = []
		for value in form.wordRelated.data:
			if form.wordRelated.data[value] != "":
				wordRelatedTemp.append(form.wordRelated.data[value])
		wordRelatedTemp.sort()
		wordInfoCopy.update({"related": wordRelatedTemp})
		wordInfoCopy.update({"relatedV": word.wordInfo["relatedV"]+1})
		# Synonyms
		wordSynonymsTemp = []
		for value in form.wordSynonyms.data:
			if form.wordSynonyms.data[value] != "":
				wordSynonymsTemp.append(form.wordSynonyms.data[value])
		wordSynonymsTemp.sort()
		wordInfoCopy.update({"synonyms": wordSynonymsTemp})
		wordInfoCopy.update({"synonymsV": word.wordInfo["synonymsV"]+1})
		# Antonyms
		wordAntonymsTemp = []
		for value in form.wordAntonyms.data:
			if form.wordAntonyms.data[value] != "":
				wordAntonymsTemp.append(form.wordAntonyms.data[value])
		wordAntonymsTemp.sort()
		wordInfoCopy.update({"antonyms": wordAntonymsTemp})
		wordInfoCopy.update({"antonymsV": word.wordInfo["antonymsV"]+1})
		# Rhymes
		wordRhymesTemp = []
		for value in form.wordRhymes.data:
			if form.wordRhymes.data[value] != "":
				wordRhymesTemp.append(form.wordRhymes.data[value])
		wordRhymesTemp.sort()
		wordInfoCopy.update({"rhymes": wordRhymesTemp})
		wordInfoCopy.update({"rhymesV": word.wordInfo["rhymesV"]+1})

		return wordInfoCopy

# Verify Word: Full
@app.route("/word/<int:wordId>/verify/full", methods=["GET", "POST"])
@login_required
def fullWordVerificationPage (wordId):
	form = WordVerificationFull()
	word = WordBank.query.get_or_404(wordId)

	print("fullWordVerificationPage")

	if form.validate_on_submit():
		wordInfoCopy = updateWordCopy(word, form, 2)

		# Update JSON Column
		word.wordInfo = wordInfoCopy
		db.session.commit()

		# Save as JSON to Words Directory
		projectDir = "/home/chsch/Documents/CODE/Tools.EFL.Coach/TEFLC v0.0.1/TEFLC"
		wordsDir = "/data/words/updated/"

		wordJSON = json.dumps(wordInfoCopy, indent=4, ensure_ascii=False)
		with open (projectDir + wordsDir + str(word.wordInfo["word"])+".json", "w") as f:
			f.write(wordJSON)
			f.close()
		
		flash("Full info for \"" + word.wordInfo["word"] + "\" verified successfully.", "alert-success")
		return redirect(url_for("wordPage", wordId=wordId))

	return render_template ("word/wordVerificationFull.html",
							title=word.word,
							word=word,
							wordId=word.id,
							form=form)


# Edit Word
@app.route("/word/<int:wordId>/edit", methods=["GET", "POST"])
@login_required
def wordEditPage (wordId):
	form = WordVerificationFull()
	word = WordBank.query.get_or_404(wordId)

	if form.validate_on_submit():
		wordInfoCopy = updateWordCopy(word, form, 2)

		# Update JSON Column
		word.wordInfo = wordInfoCopy
		db.session.commit()
		
		# Save as JSON to Words Directory
		projectDir = "/home/chsch/Documents/PYTHON/Tools.EFL.Coach/TEFLC v0.0.1/TEFLC"
		wordsDir = "/data/words/updated/"

		wordJSON = json.dumps(wordInfoCopy, indent=4, ensure_ascii=False)
		with open (projectDir + wordsDir + str(word.wordInfo["word"])+".json", "w") as f:
			f.write(wordJSON)
			f.close()
		
		flash("Changes to \"" + word.wordInfo["word"] + "\" applied successfully.", "alert-success")
		return redirect(url_for("wordPage", wordId=wordId))

	return render_template ("word/wordEdit.html",
							title=word.word,
							word=word,
							wordId=word.id,
							form=form)



# --------------------------------------------
# NO PREP APPS
# --------------------------------------------

# 5 Letter Words
@app.route("/5-Letter-Words")
def fiveLetterWordsPage ():
	return render_template("apps/5LetterWords.html",
		title="5 Letter Words")


# 20 Questions
@app.route("/20-Questions")
def twentyQsPage ():
	return render_template("apps/20Qs.html",
		title="20 Questions")

# Hot Seat
@app.route("/Hot-Seat")
def hotSeatPage ():
	return render_template("apps/hotseat.html",
		title="Hot Seat!")

# Poggle
@app.route("/Poggle")
def pogglePage ():
	return render_template("apps/poggle.html",
		title="Poggle")

# Visual Story Generator
@app.route("/Visual-Story-Generator")
def vsgPage ():
	return render_template("apps/vsg.html",
		title="Visual Story Generator")

# --------------------------------------------
# VOCABULARY APPS
# --------------------------------------------

# Unscramble
@app.route("/Unscramble")
def unscramblePage ():
	unscrambleList = []
	if current_user.is_active:
		if current_user.connected != 0:
			listQuery = WordList.query.filter_by(id=current_user.connected).first()
			print(listQuery.wordIds)
			for word in listQuery.wordIds:
				unscrambleList.append(word.word)
			# print(listQuery)
	else:
		unscrambleList = ["one", "two", "three",
					"four", "five", "six",
					"seven", "eight", "nine"]

	random.shuffle(unscrambleList)

	return render_template("apps/unscramble.html",
		title="Unscramble",
		unscrambleList=unscrambleList)


# Webapp Export
@app.route("/App-Export", methods=["GET", "POST"])
def appExportPage ():
	return render_template("apps/appExport.html",
		title="App Export")

# Word Lotto Game
@app.route("/Word-Lotto")
def wordLottoPage ():
	lottoList = []
	if current_user.is_active:
		if current_user.connected != 0:
			connectedList = WordList.query.filter_by(id=current_user.connected).first()
			if len(connectedList.wordIds) > 8:
				for x in range(9):
					lottoList.append(x.word)
			else:
				tempList = []
				for x in connectedList.wordIds:
					tempList.append(x.word)
				tempList.extend(tempList) # min: 2, max: 16
				tempList.extend(tempList) # min: 4, max: 32
				tempList.extend(tempList) # min: 8, max: 64
				tempList.extend(tempList) # min: 16, max: 128
				for x in range(9):
					lottoList.append(tempList[x])
	else:
		lottoList = ["one", "two", "three",
					"four", "five", "six",
					"seven", "eight", "nine"]

	random.shuffle(lottoList)

	return render_template("apps/wordLotto.html",
							title="Word Lotto",
							lottoList=lottoList)

# --------------------------------------------
# PRINT APPS
# --------------------------------------------

# Word Search Generator
@app.route("/Wordsearch-Generator", methods=["GET", "POST"])
def wordsearchPage ():
	form = XYInput()
	wordsearchList = []
	if current_user.is_active:
		if current_user.connected != 0:
			connectedList = WordList.query.filter_by(id=current_user.connected).first()
			for x in connectedList.wordIds:
				wordsearchList.append(x.word)
			wordsearchList.sort()
	else:
		wordsearchList = ["one", "two", "three",
					"four", "five", "six",
					"seven", "eight", "nine",
					"ten"]

	if form.validate_on_submit():
		wordsearch = generateWordSearch (wordsearchList, form.xValue.data, form.yValue.data)
	else:
		wordsearch = generateWordSearch (wordsearchList, 20, 20)

	return render_template("apps/wordsearchGenerator.html",
							title="Wordsearch Generator",
							wordsearch=wordsearch,
							form=form)
# --------------------------------------------
# CLASSROOM APPS
# --------------------------------------------

# --------------------------------------------
# YOLA APPS
# --------------------------------------------

# --------------------------------------------
