# 5
# getWordSentence.py

# --------------------------------------------
import requests
from bs4 import BeautifulSoup
import re

# --------------------------------------------
# Returns a string with a sample sentence
# Tries 3 sources
def getWordSentence (word):
	try:
		# print("A")
		# Source 1
		urlBase = "https://sentencedict.com/"
		urlSearch = urlBase + word + ".html"
		page = requests.get(urlSearch)
		soup = BeautifulSoup(page.content, 'html.parser')
		ScrapedResults = soup.find("div", id="all")
		ScrapedResults = ScrapedResults.find("div")
		sentence = ScrapedResults.text[:256]
		sentence = sentence.rstrip()
		initialPeriod = re.findall("\d\.", sentence)
		if initialPeriod:
			sentence = re.sub("\d\.", "", sentence, 1)
		else:
			sentence = re.sub("\d,", "", sentence, 1)
			sentence = re.sub("\(.\)", "", sentence, 1)
			sentence = re.sub(".\)", "", sentence, 1)
			if sentence[0].isdigit():
				sentence = sentence.lstrip("1")
		regex = re.compile("[^a-zA-Z0-9[] '!?\.,-]")
		sentence = regex.sub("", sentence)
		sentence = sentence.strip()
		if ".." in sentence:
			sentence = sentence.replace("..", ".")
	except:
		try: 
			# print("B")
			# Source 2
			urlBase = "https://www.wordhippo.com/what-is/sentences-with-the-word/"
			urlSearch = urlBase + word + ".html"
			page = requests.get(urlSearch)
			soup = BeautifulSoup(page.content, 'html.parser')
			ScrapedResults = soup.find("table", id="mainsentencestable")
			ScrapedResults = ScrapedResults.find("td")
			sentence = ScrapedResults.text[:256]
		except:
			try:
				# print("C")
				# Source 3
				urlBase = "https://sentence.yourdictionary.com/"
				urlSearch = urlBase + word
				page = requests.get(urlSearch, timeout=(0.5, 1.0))
				soup = BeautifulSoup(page.content, 'html.parser')
				ScrapedResults = soup.find("div", class_="sentence component")
				sentence = ScrapedResults.text[:256]	
			except:
				sentence = ""
	return sentence

# --------------------------------------------
# sentence = getWordSentence("cat") #A
# sentence = getWordSentence("calico cat") #B
# sentence = getWordSentence("covid") #C
# print(sentence)