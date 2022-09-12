# 8
# getAntonyms.py

# --------------------------------------------
import requests
import datamuse
from bs4 import BeautifulSoup
import re

# --------------------------------------------
api = datamuse.Datamuse()
api.set_max_default(20)

# --------------------------------------------
# Returns a sorted list of top 10 antonyms
# Tries 3 sources
def getAntonyms (word):
	regex = re.compile("[^a-zA-Z0-9[] '!?\.,-]")
	antonyms = []
	antonymCount = 0
	try: 
		# print("A")
		# Source 1
		urlBase = "https://www.thesaurus.com/browse/"
		urlSearch = urlBase + word
		page = requests.get(urlSearch)
		soup = BeautifulSoup(page.content, 'html.parser')
		ScrapedResults = soup.find("div", id="antonyms")
		ScrapedResults = ScrapedResults.find("ul", class_="et6tpn80")
		for child in ScrapedResults.children:
			if antonymCount < 10:
				tempWord = child.text
				tempWord = regex.sub("", tempWord)
				tempWord = tempWord.strip()
				if tempWord not in antonyms:
					antonyms.append(tempWord)
					antonymCount += 1
		if antonymCount < 10:
			# print("B")
			# Source 2
			urlBase = "https://www.merriam-webster.com/thesaurus/"
			urlSearch = urlBase + word
			page = requests.get(urlSearch)
			soup = BeautifulSoup(page.content, 'html.parser')
			ScrapedResults = soup.find_all("span", class_="thes-list opp-list") 
			for result in ScrapedResults:
				ants = result.find_all("a")
				for ant in ants:
					if antonymCount < 10:
						tempWord = ant.text
						tempWord = regex.sub("", tempWord)
						tempWord = tempWord.strip()
						if tempWord not in antonyms:
							antonyms.append(tempWord)
							antonymCount += 1
		if antonymCount < 10:
			# print("C")
			# Source 3
			apitest = api.words(rel_ant=word)
			for result in apitest:
				tempWord = result["word"]
				if antonymCount < 10:
					if tempWord not in antonyms:
						antonyms.append(result["word"])
						antonymCount += 1
	except:
		try:
			# print("BB == B")
			# Source 2 if Source 1 failed
			urlBase = "https://www.merriam-webster.com/thesaurus/"
			urlSearch = urlBase + word
			page = requests.get(urlSearch)
			soup = BeautifulSoup(page.content, 'html.parser')
			ScrapedResults = soup.find_all("span", class_="thes-list opp-list") 
			for result in ScrapedResults:
				ants = result.find_all("a")
				for ant in ants:
					if antonymCount < 10:
						tempWord = ant.text
						tempWord = regex.sub("", tempWord)
						tempWord = tempWord.strip()
						if tempWord not in antonyms:
							antonyms.append(tempWord)
							antonymCount += 1
			if antonymCount < 10:
				# print("CC == C")
				# Source 3
				apitest = api.words(rel_ant=word)
				for result in apitest:
					tempWord = result["word"]
					if antonymCount < 10:
						if tempWord not in antonyms:
							antonyms.append(result["word"])
							antonymCount += 1
		except:
			# print("CCC")
			# Source 3
			apitest = api.words(rel_ant=word)
			for result in apitest:
				tempWord = result["word"]
				if antonymCount < 10:
					if tempWord not in antonyms:
						antonyms.append(tempWord)
						antonymCount += 1
	antonyms.sort()
	return antonyms

# --------------------------------------------

'''
word = "finally"
antonyms = getAntonyms(word)

print("-----------------")
print(word, str(len(antonyms)))
print("-----------------")
print(antonyms)
print("-----------------")
'''