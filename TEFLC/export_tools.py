# export_tools.py
# Converts vocabulary data to XLS / CSV formats.
# ----------------------------------------

# References
# https://realpython.com/openpyxl-excel-spreadsheets-python/
# https://realpython.com/python-csv/
# https://openpyxl.readthedocs.io/en/stable/styles.html#colours

# ----------------------------------------

# Imports
from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment, Border, Side, colors
import random, os, json, csv

# My Files
from export_tools.third_party_classes import Gimkit_1, Gimkit_2, Quizizz, Kahoot
# 

# ----------------------------------------
# Load Word JSON file for testing
# On TEFLC can just query db

def use_word (word):
	project_dir = "/home/chsch/Documents/PYTHON/Tools.EFL.Coach/TEFLC v0.0.1/TEFLC"
	words_dir = "/data/words/original/"
	f = open(project_dir + words_dir + str(word)+".json")
	data = json.load(f)
	return data

# ----------------------------------------
# Questions
# Produces a question for a given word and choice of word info.

def question_gen (choice, word_info):

	questions_word = {
		1: "Which is the IPA spelling of \"{}\"?".format(word_info["word"]),
		2: "What part of speech is \"{}\"?".format(word_info["word"]),
		3: "Which is the definition of \"{}\"?".format(word_info["word"]),
		4: "How many syllables does \"{}\" have?".format(word_info["word"]),
		5: "Which is a synonym of \"{}\"?".format(word_info["word"]),
		6: "Which is an antonym of \"{}\"?".format(word_info["word"]),
		7: "Which word rhymes with \"{}\"?".format(word_info["word"])
	}

	# ! : Have to figure out how to use this.
	questions_no_word = {
		1: "{}".format(word_info["ipa"]),
		2: "Which word is a {}?".format(word_info["type"]),
		3: "\"{}\"".format(word_info["definition"]),
		4: "A {} syllable word:".format(word_info["syllables"]),
		5: "A synonym of \"{}\":".format(word_info["synonyms"]),
		6: "An antonym of \"{}\":".format(word_info["antonyms"]),
		7: "Which word rhymes with \"{}\"?".format(word_info["rhymes"])
	}

	# !: Shouldn't use random because need to track the type / value
	if choice == 0:
		return questions_word[random.randrange(1,7)]
	
	else:
		return questions_word[choice]


# ----------------------------------------
# Testing 
# ----------------------------------------

# Sample Request Data
# Data from form submit.
request = {
	"site": 3, # Gimkit
	"content": [3], # Definition
	"randomize": [1,2], # Qs and Content
	"total_questions": 5,
	"time_per_question": 30 # Not for Gimkit
}

word_list = ["apple", "banana", "cherry", "mango", "orange", "pear"]

# Initialize workbook and sheet
workbook = Workbook()
sheet = workbook.active

# Choose Third Party Class for sheet
if request["site"] == 1:
	sheet = Kahoot.default_sheet(sheet)
elif request["site"] == 2:
	sheet = Quizizz.default_sheet(sheet)
elif request["site"] == 3:
	sheet = Gimkit_2.default_sheet(sheet)

# six words -> need ten
for count, word in enumerate(word_list):

	if count+1 > request["total_questions"]:
		break
	print(count+1)

	# get word info
	word_info = use_word(word)

	# get question
	question = question_gen(3, word_info) # definition

	# create incorrect answers
	# :: !! import !! ::

	# create class instance
	# Gimkit 1
	gimkit_question = Gimkit_1(question, 
								word_info["definition"], 
								answer_incorrect_1, 
								answer_incorrect_2,
								answer_incorrect_3)

	print(gimkit_question.question)
	print(gimkit_question.answer_correct)
	print(gimkit_question.answer_incorrect_1)
	print(gimkit_question.answer_incorrect_2)
	print(gimkit_question.answer_incorrect_3)


	# add to sheet
	# Gimkit 1
	sheet = Gimkit_1.add_question(sheet, count, 
						gimkit_question.question, 
						gimkit_question.answer_correct,
						gimkit_question.answer_incorrect_1,
						gimkit_question.answer_incorrect_2,
						gimkit_question.answer_incorrect_3)

	# create class instance
	# Gimkit 2
	# gimkit_question = Gimkit_2(question, word_info["definition"])
	# print(gimkit_question.question)
	# print(gimkit_question.answer_correct)

	# add to sheet
	# Gimkit 2
	# sheet = Gimkit_2.add_question(sheet, count, 
	# 					gimkit_question.question, 
	# 					gimkit_question.answer_correct)

# Save Workbook
if request["site"] == 1:
	Kahoot.save_workbook(workbook)
elif request["site"] == 2:
	Quizizz.save_workbook(workbook)
elif request["site"] == 3:
	Gimkit_2.save_workbook(workbook)


'''
# Test Question for Gimkit 1
gimkit_question_2 = Gimkit_1(question, 
		word_info["definition"],
		"pear", "peach", "plum")
print(gimkit_question_2.question)
print(gimkit_question_2.answer_correct)
'''

# ----------------------------------------