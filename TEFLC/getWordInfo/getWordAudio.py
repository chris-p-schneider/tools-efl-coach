# 0B
# getWordAudio.py

# --------------------------------------------
import requests
from bs4 import BeautifulSoup
import json

# --------------------------------------------
# Returns a URL to audio file as string
def getWordAudio (word):
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
		wordAudio = jsonInfo["phonetics"][0]["audio"]
	
	except:
		wordAudio = ""
		
	return wordAudio

# --------------------------------------------
# wordAudio = getWordAudio("correct") #A
# wordAudio = getWordAudio("I don't know") #Fail
# print(wordAudio)