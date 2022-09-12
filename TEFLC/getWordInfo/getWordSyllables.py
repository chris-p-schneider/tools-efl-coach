# 4
# getWordSyllables.py

# --------------------------------------------
import requests
from bs4 import BeautifulSoup
from pysyllables import get_syllable_count
# import eng_to_ipa as ipa 
# ipa.syllable_count(word)

# --------------------------------------------
# Returns an int of word syllables
# Tries 2 sources
# Required for rhymingWords()
def getWordSyllables (word):
	wordSyllables = 0
	# Check if word is actually phrase
	if " " in word:
		# print("a")
		# Try syllable package first
		tempWordList = word.split()
		for item in tempWordList:
			tempSyllables = get_syllable_count(item)
			if tempSyllables == None:
				pass
			else:
				wordSyllables = wordSyllables + tempSyllables
		# Fallback to scraping
		if wordSyllables == 0:
			# print("b")
			# Source 2
			urlBase = "http://www.syllablecount.com/syllables/"
			urlSearch = urlBase + word
			try:
				page = requests.get(urlSearch)
				soup = BeautifulSoup(page.content, 'html.parser')
				ScrapedResults = soup.find(id="ctl00_ContentPane_paragraphtext").contents[1]
				wordSyllables = int(ScrapedResults.text)
			except:
				wordSyllables = 0
	# If word is actually one word
	else:
		# print("A")
		wordSyllables = get_syllable_count(word)
		if wordSyllables == None:
			# print("B")
			urlBase = "http://www.syllablecount.com/syllables/"
			urlSearch = urlBase + word
			try: 
				page = requests.get(urlSearch)
				soup = BeautifulSoup(page.content, 'html.parser')
				ScrapedResults = soup.find(id="ctl00_ContentPane_paragraphtext").contents[1]
				wordSyllables = int(ScrapedResults.text)
			except:
				wordSyllables = 0
	return wordSyllables

# --------------------------------------------
# wordSyllables = getWordSyllables("exciting") #A 
# wordSyllables = getWordSyllables("weifoenc") #B
# print(wordSyllables)