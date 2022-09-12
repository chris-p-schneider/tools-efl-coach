# 7
# getSynonyms.py

# --------------------------------------------
import requests
import datamuse
from bs4 import BeautifulSoup

# --------------------------------------------
api = datamuse.Datamuse()
api.set_max_default(50)

# --------------------------------------------
# Returns a sorted list of top 10 synonyms
# Tries 2 sources
def getSynonyms (word):
	synonyms = []
	synonymCount = 0
	try:
		# print("A")
		# Source 1
		urlBase = "https://www.thesaurus.com/browse/"
		urlSearch = urlBase + word
		page = requests.get(urlSearch)
		soup = BeautifulSoup(page.content, 'html.parser')
		ScrapedResults = soup.find("ul", class_="et6tpn80")
		try:
			# Check if no results
			noResults = soup.find("h2", class_="spell-suggestions-subtitle")
			if noResults.text[0] == 'D':
				pass
		except:
			# Results valid
			for child in ScrapedResults.children:
				if synonymCount < 10:
					tempWord = child.contents[0].text
					tempWord = tempWord.strip()
					if tempWord not in synonyms:
						synonyms.append(tempWord)
						synonymCount += 1
			# print(word, str(synonymCount))
			# print(synonyms)
			# print("B")
			# Source 2
			if synonymCount < 10:
				apitest = api.words(rel_syn=word)
				for result in apitest:
					tempWord = result["word"]
					if synonymCount < 10:
						if tempWord not in synonyms:
							synonyms.append(tempWord)
							synonymCount += 1
			# print(word, str(synonymCount))
	except:
		# print("B2 == B")
		apitest = api.words(rel_syn=word)
		for result in apitest:
			tempWord = result["word"]
			if tempWord not in synonyms:
				synonyms.append(tempWord)
				synonymCount += 1

	synonyms.sort()
	return synonyms

# --------------------------------------------

'''
word = "cousin"

# synonyms = getSynonyms("World War II") #A
# synonyms = getSynonyms("cousin") #B

synonyms = getSynonyms(word)
print("---------------------")
print(word, str(len(synonyms)))
print("---------------------")
print(synonyms)
print("---------------------")
'''