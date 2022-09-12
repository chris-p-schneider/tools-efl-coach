# 0
# getWordIpa.py

# --------------------------------------------
import requests
from bs4 import BeautifulSoup
import eng_to_ipa as ipa
import json
# https://github.com/nordnet/python-freeipa-json
# Consideration ^ 

# --------------------------------------------
# Returns a string of the word in IPA
# Checks 2 sources
def getWordIPA (word):
	try:
		# print("A")
		# Source 1: API scraper
		urlBase = "https://api.dictionaryapi.dev/api/v2/entries/en/"
		urlSearch = urlBase + word
		page = requests.get(urlSearch)
		soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf-8")
		soup = soup.text
		jsonInfo = json.loads(soup)
		jsonInfo = jsonInfo[0]
		wordIPA = jsonInfo["phonetics"][0]["text"]
	
	except:
		# print("B")
		# Source 2: IPA Package
		wordIPA = ipa.jonvert(word)
		# not sure if linguistically correct but it matches the former
		wordIPA = '/' + wordIPA + '/'

	return wordIPA

# --------------------------------------------

# word = "nice"
# print(word)

# wordIPA = getWordIPA(word) #A
# wordIPA = getWordIPA("I don't know") #B
# print(wordIPA)