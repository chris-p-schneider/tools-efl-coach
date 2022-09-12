# 5letterwords.py
'''
1 picks a 5 letter word
2 user inputs a word
3 shows matching letters
4 user inputs a word until
5 the word is matched
'''

#-------------------------------------------
# IMPORTS
import os, os.path, json
import datamuse
from tqdm import tqdm

#-------------------------------------------
# DATAMUSE
api = datamuse.Datamuse()

#-------------------------------------------
# JSON DICTIONARY
directory = "/home/chsch/Documents/PYTHON/Tools.EFL.Coach/TEFLC v0.0.1/TEFLC/static/test/"
filepath = directory + "dictionary.json"

with open (filepath, "r") as dictionary:
	data = dictionary.read()

dictObj = json.loads(data)

#-------------------------------------------
# VARIABLES
fiveLetterWords = {} # number: word 
fiveLetterWordsScored = {} # word: score
bestFiveLetterWords = {} # word: score

#-------------------------------------------
# GET 5 LETTER WORDS FROM DICT
for count, key in enumerate(dictObj):
	if len(key) == 5:
		fiveLetterWords.update({count: key})
#-------------------------------------------
# ADD SCORES TO DICT
def addScores(fiveLetterWords, fiveLetterWordsScored, bestFiveLetterWords):
	with tqdm(total=100) as pbar:
		for count, key in enumerate(fiveLetterWords):
			if count > 12:
				pass
			tempWord = fiveLetterWords[key]
			freq = api.words(sp=tempWord, max=1, md="f")
			freqNum = round(float(freq[0]["tags"][0][2:8]), 2)
			if freqNum > 0:
				fiveLetterWordsScored.update({tempWord: freqNum})
				print("Added {} ({}) to scored dict." .format(tempWord, freqNum))
				print("There are now {} scored out of {} total." .format(len(fiveLetterWordsScored), len(fiveLetterWords)))
				if freqNum > 5:
					bestFiveLetterWords.update({tempWord: freqNum})
					print("-----")
					print("Added {} ({}) to best words dict." .format(tempWord, freqNum))
					print("There are now {} best words out of {} total." .format(len(bestFiveLetterWords), len(fiveLetterWordsScored)))
			pbar.update(round(1/len(fiveLetterWords), 2))
			print(" ")

#-------------------------------------------
# WRITE TO JSON
def writeJSON(fiveLetterWordsScored, bestFiveLetterWords):
	fiveLetterWordsScoredJSON = json.dumps(fiveLetterWordsScored, indent=4, ensure_ascii=False)
	with open (directory + "five-letter-words/" + "fiveLetterWordsScored.json", "w") as f:
		f.write(fiveLetterWordsScoredJSON)
		f.close()

	bestFiveLetterWordsJSON = json.dumps(bestFiveLetterWords, indent=4, ensure_ascii=False)
	with open (directory + "five-letter-words/" +"bestFiveLetterWords.json", "w") as f:
		f.write(bestFiveLetterWordsJSON)
		f.close()

#-------------------------------------------
# PRINT WORDS
def printResults(dictObj, fiveLetterWords, fiveLetterWordsScored, bestFiveLetterWords):
	print("--------------------------------------")
	print("There are {} total words, {} five-letter words.".upper() .format(len(dictObj), len(fiveLetterWords)))
	print("{} five-letter words scored above 0:".upper() .format(len(fiveLetterWordsScored)))
	print("--------------------------------------")
	for value, key in enumerate(fiveLetterWordsScored, start=1):
		print(value, "-", key, "(", fiveLetterWordsScored[key], ")")

	print("--------------------------------------")
	print("{} five-letter words scored above 5:".upper() .format(len(bestFiveLetterWords)))
	print("--------------------------------------")
	for value, key in enumerate(bestFiveLetterWords, start=1):
		print(value, "-", key, "(", bestFiveLetterWords[key], ")")

	print("--------------------------------------")

#-------------------------------------------
# RUN MAIN
print("========================================")
print("Adding scores to five-letter words...")
print("========================================")
addScores(fiveLetterWords, fiveLetterWordsScored, bestFiveLetterWords)
print("========================================")
print("Writing JSON to file...")
print("========================================")
writeJSON(fiveLetterWordsScored, bestFiveLetterWords)
print("Printing results...")
print("========================================")
printResults(dictObj, fiveLetterWords, fiveLetterWordsScored, bestFiveLetterWords)
print("========================================")
print("All finished!")
print("========================================")