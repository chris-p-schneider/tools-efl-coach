# wordInfo.py
# Generate / Scrape default word info.
# --------------------------------------------
# Input: iterable wordlist
# Output: JSON file for each word

# --------------------------------------------
# IMPORTS
# --------------------------------------------
import googletrans
from googletrans import Translator
import time
from tqdm import tqdm
import json
import os.path

# --------------------------------------------
# MY IMPORTS
# --------------------------------------------
from TEFLC.getWordInfo.getWordIpa import getWordIPA # string
from TEFLC.getWordInfo.getWordAudio import getWordAudio # string
from TEFLC.getWordInfo.getWordType import getWordType # string
from TEFLC.getWordInfo.getWordDef import getWordDef # string
from TEFLC.getWordInfo.getWordImgs import getWordImgs # ?
from TEFLC.getWordInfo.getWordSyllables import getWordSyllables # int
from TEFLC.getWordInfo.getWordSentence import getWordSentence # string
from TEFLC.getWordInfo.getRelatedWords import getRelatedWords # list
from TEFLC.getWordInfo.getSynonyms import getSynonyms # list
from TEFLC.getWordInfo.getAntonyms import getAntonyms # list
from TEFLC.getWordInfo.getRhymingWords import getRhymingWords # list !

# --------------------------------------------
# FUNCTIONS
# --------------------------------------------

# Gets all word info
# Saves to dictionary
def getWordInfo (word):
	start = time.time()
	print("Adding info for \"{}\"." .format(word))

	# Making this iterable for tqdm
	infoKeys = ["word", "wordV", "ipa", "audio",
				"type", "typeV", "definition",
				"definitionV", "images", "imagesV", 
				"imageSelected", "syllables", "syllablesV",
				"sentence", "sentenceV", "related",
				"relatedV", "synonyms", "synonymsV",
				"antonyms", "antonymsV", "rhymes", 
				"rhymesV"]
	
	infoValues = {
		0: word, 1: 0,
		2: getWordIPA,	3: getWordAudio,
		4: getWordType,	5: 0, 6: getWordDef,
		7: 0, 8: getWordImgs, 9: 0, 10: "", 
		11: getWordSyllables, 12: 0, 
		13: getWordSentence, 14: 0,
		15: getRelatedWords, 16: 0, 
		17: getSynonyms, 18: 0, 
		19: getAntonyms, 20: 0,
		21: getRhymingWords, 22: 0
	}
	
	wordDict = {}
	skipList = [0,1,5,7,9,10,12,14,16,18,20,22]

	with tqdm(total=100) as pbar:
		for i in (range(23)):
			stepStart = time.time()
			# print(infoKeys[i])
			# print(infoValues[i])
			if i in skipList:
				wordDict[infoKeys[i]] = infoValues[i]
				print(str(infoValues[i]))
			else:
				wordDict[infoKeys[i]] = infoValues[i](word)
				print(str(infoValues[i]))
			stepStop = time.time()
			stepTime = round((stepStop-stepStart), 2)
			print("{} took {} to complete." .format(infoKeys[i], stepTime))
			print("-----------------------")
			pbar.update(round(4.347, 3))
	'''
	wordDict = {
		"word": word,
		"wordV": 0,
		"ipa": getWordIPA(word),
		"audio": getWordAudio(word),
		"type": getWordType(word),
		"typeV": 0,
		"definition": getWordDef(word),
		"definitionV": 0,
		"images": [], #!!!
		"imageV": 0,
		"imageSelected": "",
		"syllables": getWordSyllables(word),
		"syllablesV": 0,
		"sentence": getWordSentence(word),
		"sentenceV": 0,
		"related": getRelatedWords(word),
		"relatedV": 0,
		"synonyms": getSynonyms(word),
		"synonymsV": 0,
		"antonyms": getAntonyms(word),
		"antonymsV": 0,
		"rhymes": getRhymingWords(word),
		"rhymesV": 0
	}
	'''
	end = time.time()
	seconds = end-start
	seconds = round(seconds, 2)

	print("---------------")
	print("Word Info added for \"{}\" in {} seconds." .format(word, seconds))
	print("---------------")

	# Save as JSON to Words Directory
	projectDir = "/TEFLC v0.0.1/TEFLC"
	wordsDir = "/data/words/original/"

	wordJSON = json.dumps(wordDict, indent=4, ensure_ascii=False)
	with open (projectDir + wordsDir + str(word)+".json", "w") as f:
		# Learn to change filepath
		f.write(wordJSON)
		f.close()

	return wordDict

# --------------------------------------------
# Gets word info for all words in a list
def getListInfo (words):
	start = time.time()

	projectDir = "/TEFLC v0.0.1/TEFLC"
	wordsDir = "/data/words/original/"
	count = 1

	for word in tqdm(words):
		print("Getting info for \"{}\"! [{} of {}]..." .format(word, count, len(words)))
		print("...")
		wordDict = getWordInfo(word)
		wordJSON = json.dumps(wordDict, indent=4, ensure_ascii=False)
		# print(wordJSON)
		# print(wordJSON.encode("ascii"))
		with open (projectDir + wordsDir + str(word)+".json", "w") as f:
			# Learn to change filepath
			f.write(wordJSON)
			f.close()
		count += 1

	end = time.time()
	seconds = end-start
	seconds = round(seconds, 2)
	
	print("---------------")
	print("{} words completed in {} seconds." .format(len(words), seconds))
	print("That's {} minutes." .format(round((seconds/60), 2)))
	print("That's an average of {} seconds per word." .format(round((seconds / len(words)), 2)))
	print("---------------")

# --------------------------------------------
# RUN
# --------------------------------------------

# word = "art"
# testDict = getWordInfo(word)
# print(testDict)

# --------------------------------------------

# word = "immigrant"
'''
listString = ""
listString = listString.strip()
words = listString.split('\n')
# words = ["word1", "word2", "word3"]
getListInfo(words)
'''

# --------------------------------------------
# ALERTS
# -> compound words with space
# -> type = preposition

# --------------------------------------------
# TYPES OF MANAUAL CORRECTIONS
'''
wrong word type or mixed word type
	clone hmm

wrong syllables (unlikely)

definition for homophone

unrelated related words

rhyming words inappropriate, 
	too complicated, 
	or need capitalization

sample sentence formatting or relevance

synonyms or antonyms too irrelevant 
	or not human enough

'''