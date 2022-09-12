# 2
# getWordDef.py

# --------------------------------------------
import requests
from bs4 import BeautifulSoup
import re

# --------------------------------------------
# Returns a string of the word definition
# Tries 3 sources
def getWordDef (word):
	# print("A")
	# Source 1
	urlBase = "https://www.learnersdictionary.com/definition/"
	urlSearch = urlBase + word
	page = requests.get(urlSearch)
	soup = BeautifulSoup(page.content, 'html.parser')
	try: 
		ScrapedResults = soup.find("span", class_="def_text")
		wordDef = ""
		wordDef = ScrapedResults.text[:256]
	except:
		try:
			# print("B")
			# Source 2
			urlBase = "https://www.dictionary.com/browse/"
			urlSearch = urlBase + word
			page = requests.get(urlSearch)
			soup = BeautifulSoup(page.content, 'html.parser')
			ScrapedResults = soup.find("span", class_="one-click-content")
			wordDef = ""
			wordDef = ScrapedResults.text[:256]
		except:
			try: 
				# print("C")
				# Source 3
				urlBase = "https://simple.wikipedia.org/wiki/"
				urlSearch = urlBase + word
				page = requests.get(urlSearch)
				soup = BeautifulSoup(page.content, 'html.parser')
				ScrapedResults = soup.find("div", class_="mw-parser-output")
				ScrapedResults = ScrapedResults.find("p")
				wordDef = ""
				wordDef = ScrapedResults.text[:256]
				regex = re.compile("[^a-zA-Z0-9[] '!?\.-]")
				wordDef = regex.sub("", wordDef)
				citations = re.findall("\[.\]", wordDef)
				for citation in citations:
					wordDef = wordDef.replace(citation, "")
				wordDefList = wordDef.split(".")
				tempSentences = ""
				counter = 0
				for sentence in wordDefList:
					if counter < len(wordDefList)-1:
						tempSentences = tempSentences + sentence + "."
						counter += 1
					else:
						pass
				wordDef = tempSentences
				if "   " in wordDef:
					wordDef = wordDef.replace("   ", " ")
				elif "  " in wordDef:
					wordDef = wordDef.replace("  ", " ")
			except: 
				wordDef = ""
	return wordDef

# --------------------------------------------
# wordDef = getWordDef("cat") #A
# wordDef = getWordDef("colour") #B
# wordDef = getWordDef("calico sheep") #C
# print(wordDef)