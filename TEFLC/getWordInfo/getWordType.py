# 1
# getWordType.py

# --------------------------------------------
import requests
import datamuse
from bs4 import BeautifulSoup
import re
import json

# --------------------------------------------
api = datamuse.Datamuse()
api.set_max_default(10)
# --------------------------------------------

# Returns a string of the word type
# Tries 5 sources
def getWordType (word):
	try:
		# print("A")
		# Source 1: unoffical gDict API
		urlBase = "https://api.dictionaryapi.dev/api/v2/entries/en/"
		urlSearch = urlBase + word
		page = requests.get(urlSearch)
		soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf-8")
		soup = soup.text
		jsonInfo = json.loads(soup)
		jsonInfo = jsonInfo[0]
		wordType = jsonInfo["meanings"][0]["partOfSpeech"]
	except:
		try:
			# print("B")
			# Source 2: Datamuse API
			apiType = api.words(sp=word, md="p", max=1)
			if apiType != []:
				wordType = apiType[0]["tags"][0]
				if wordType == "n":
					wordType = "noun"
				elif wordType == "v":
					wordType = "verb"
				elif wordType == "adj":
					wordType = "adjective"
				elif wordType == "adv":
					wordType = "adverb"
				else:
					wordType = ""
			if apiType == [] or wordType == "":
				try:
					# print("C")
					# Source 3
					urlBase = "https://www.freethesaurus.com/"
					urlSearch = urlBase + word
					page = requests.get(urlSearch)
					soup = BeautifulSoup(page.content, 'html.parser')
					wordResult = soup.find("span", class_="TPSP")
					wordType = wordResult.text
					# Reformat if necessary
					if wordType == "adj":
						wordType = "adjective"
					elif wordType == "adv":
						wordType = "adverb"
					elif wordType == "prep":
						wordType = "preposition"
				except:
					try:
						# print("D")
						# Source 4
						urlBase = "https://www.learnersdictionary.com/definition/"
						urlSearch = urlBase + word
						page = requests.get(urlSearch)
						soup = BeautifulSoup(page.content, 'html.parser')
						wordResult = soup.find("span", class_="hw_txt gfont")
						theWord = wordResult.text
						theWord = theWord.strip()
						pluralForms = soup.find("div", class_="hw_infs_d")
						pluralWords = pluralForms.find_all("span", class_="i_text")
						pluralWordString = ""
						for plural in pluralWords:
							pluralWordString = pluralWordString + plural.text + " "
						wordType = ""
						if word == theWord:
							ScrapedResults = soup.find("span", class_="fl")
							wordType = ScrapedResults.text[:64]
						elif word in pluralWordString:
							ScrapedResults = soup.find("span", class_="fl")
							wordType = ScrapedResults.text[:64]
						else:
							otherWordsDivs = soup.find_all("div", class_="uro_line")
							otherWords = soup.find_all("h2", class_="ure")
							otherWordCounter = 0
							for other in otherWords:
								regex = re.compile("[^a-zA-Z '!?\.-]")
								otherWord = other.text
								otherWord = regex.sub("", otherWord)
								otherWord = otherWord.lstrip()
								if otherWord == word:
									break
								otherWordCounter += 1
							otherWordDivCounter = 0
							for div in otherWordsDivs:
								if otherWordDivCounter == otherWordCounter:
									ScrapedResults = div.find("span", class_="fl")
									wordType = ScrapedResults.text[:64]
								otherWordDivCounter += 1
					except:
						try: 
							# print("E")
							# Source 5
							urlBase = "https://www.dictionary.com/browse/"
							urlSearch = urlBase + word
							page = requests.get(urlSearch)
							soup = BeautifulSoup(page.content, 'html.parser')
							ScrapedResults = soup.find("span", class_="luna-pos")
							wordType = ""
							wordType = ScrapedResults.text[:64]
							regex = re.compile("[^a-zA-Z '!?\.-]")
							wordType = regex.sub("", wordType)
						except:
							wordType = ""
		except:
			try:
				# print("CC")
				# Source 3
				urlBase = "https://www.freethesaurus.com/"
				urlSearch = urlBase + word
				page = requests.get(urlSearch)
				soup = BeautifulSoup(page.content, 'html.parser')
				wordResult = soup.find("span", class_="TPSP")
				wordType = wordResult.text
				# Reformat if necessary
				if wordType == "adj":
					wordType = "adjective"
				elif wordType == "adv":
					wordType = "adverb"
				elif wordType == "prep":
					wordType = "preposition"
			except:
				try:
					# print("DD")
					# Source 4
					urlBase = "https://www.learnersdictionary.com/definition/"
					urlSearch = urlBase + word
					page = requests.get(urlSearch)
					soup = BeautifulSoup(page.content, 'html.parser')
					wordResult = soup.find("span", class_="hw_txt gfont")
					theWord = wordResult.text
					theWord = theWord.strip()
					pluralForms = soup.find("div", class_="hw_infs_d")
					pluralWords = pluralForms.find_all("span", class_="i_text")
					pluralWordString = ""
					for plural in pluralWords:
						pluralWordString = pluralWordString + plural.text + " "
					wordType = ""
					if word == theWord:
						ScrapedResults = soup.find("span", class_="fl")
						wordType = ScrapedResults.text[:64]
					elif word in pluralWordString:
						ScrapedResults = soup.find("span", class_="fl")
						wordType = ScrapedResults.text[:64]
					else:
						otherWordsDivs = soup.find_all("div", class_="uro_line")
						otherWords = soup.find_all("h2", class_="ure")
						otherWordCounter = 0
						for other in otherWords:
							regex = re.compile("[^a-zA-Z '!?\.-]")
							otherWord = other.text
							otherWord = regex.sub("", otherWord)
							otherWord = otherWord.lstrip()
							if otherWord == word:
								break
							otherWordCounter += 1
						otherWordDivCounter = 0
						for div in otherWordsDivs:
							if otherWordDivCounter == otherWordCounter:
								ScrapedResults = div.find("span", class_="fl")
								wordType = ScrapedResults.text[:64]
							otherWordDivCounter += 1
				except:
					try: 
						# print("EE")
						# Source 5
						urlBase = "https://www.dictionary.com/browse/"
						urlSearch = urlBase + word
						page = requests.get(urlSearch)
						soup = BeautifulSoup(page.content, 'html.parser')
						ScrapedResults = soup.find("span", class_="luna-pos")
						wordType = ""
						wordType = ScrapedResults.text[:64]
						regex = re.compile("[^a-zA-Z '!?\.-]")
						wordType = regex.sub("", wordType)
					except:
						wordType = ""

	return wordType

# --------------------------------------------
# wordType = getWordType("friendship") #A
# wordType = getWordType("?") #B
# wordType = getWordType("?") #C
# wordType = getWordType("yeet") #D
# wordType = getWordType("got off") #Error prior
# print(wordType)