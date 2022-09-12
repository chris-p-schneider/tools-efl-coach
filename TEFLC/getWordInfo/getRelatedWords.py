# 6
# getRelatedWords.py

# --------------------------------------------
import requests
import datamuse
from bs4 import BeautifulSoup
import re

# --------------------------------------------
api = datamuse.Datamuse()
api.set_max_default(20)

# --------------------------------------------
# Returns string of reduced word
def wordReducer(word):
	originalLength = len(word)
	searchLength = 0
	# Adjust for length / suffix
	if originalLength <5:
		if word[originalLength-1] == "s":
			searchLength = originalLength - 1
		else:
			searchLength = originalLength
	elif originalLength < 7:
		searchLength = originalLength - 1
	elif originalLength < 11:
		if word[originalLength-1] == "s":
			searchLength = originalLength - 1
		else:
			searchLength = originalLength - 3
	else:
		if word[originalLength-3:originalLength] == "ing":
			searchLength = originalLength-3
		else:
			searchLength = originalLength - 5
	# Rejoin word as reduced
	reducedWord = ""
	counter = 0
	# print("-------------------")
	# print("counter, searchLength, originalLength")
	# print(counter, searchLength, originalLength)
	# print("-------------------")
	for c in word:
		if counter < searchLength:
			reducedWord = reducedWord + c
		counter += 1
	# Handle spelling changes
	if reducedWord[len(reducedWord)-1] == reducedWord[len(reducedWord)-2]:
		reducedWord = reducedWord[0:len(reducedWord)-1]

	return reducedWord


# --------------------------------------------
# Returns a list of top 10 related words
# Tries 2 sources
def getRelatedWords (word):
	regex = re.compile("[^a-zA-Z '!?\.-]")
	relatedWords = []
	wordCount = 0
	try:
		# print("A")
		# Source 1
		urlBase = "https://www.merriam-webster.com/dictionary/"
		urlSearch = urlBase + word
		page = requests.get(urlSearch)
		soup = BeautifulSoup(page.content, 'html.parser')
		ScrapedResults = soup.find_all("span", class_="if")
		for span in ScrapedResults:
			tempWord = span.text
			tempWord = regex.sub("", tempWord)
			tempWord = tempWord.strip()
			if wordCount < 10:
				if tempWord not in relatedWords:
					if tempWord != word:
						relatedWords.append(tempWord)
						wordCount += 1
		# Continue to 10 related words
		# print(wordCount)
		# print(relatedWords)
		if wordCount < 10:
			# print("B")
			# Source 2
			urlBase = "https://www.dictionary.com/browse/"
			urlSearch = urlBase + word
			page = requests.get(urlSearch)
			soup = BeautifulSoup(page.content, 'html.parser')
			ScrapedResults = soup.find_all("span", class_="luna-runon bold")
			for span in ScrapedResults:
				tempWord = span.text
				tempWord = regex.sub("", tempWord)
				tempWord = tempWord.strip()
				if wordCount < 10:
					if tempWord not in relatedWords:
						if tempWord != word:
							relatedWords.append(tempWord)
							wordCount += 1
			# print(wordCount)
			# print(relatedWords)
			if wordCount < 10:
				# print("C")
				# Source 3: API
				reducedWord = wordReducer(word)
				apitest = api.words(sp=str(reducedWord)+'*')
				# print(word, reducedWord)
				# print(apitest)
				# print("--------------")
				for item in apitest:
					if wordCount < 10:
						tempWord = item["word"]
						# print(tempWord)
						if tempWord not in relatedWords:
							if tempWord == word:
								pass
							else:
								relatedWords.append(tempWord)
								wordCount += 1
				# print(wordCount)
				# print(relatedWords)
			# If still < 10 related words:
			# Add probably unrelated words
			# Print("BB")
			if wordCount < 10:
				ScrapedResults = soup.find("div", class_="css-1foc103 e14wda90")
				nearbyWords = ScrapedResults.find_all("a", class_="css-6xix1i e14wda92")
				for a in nearbyWords:
					tempWord = a.text
					tempWord = regex.sub("", tempWord)
					tempWord = tempWord.strip()
					if wordCount < 10:
						if tempWord not in relatedWords:
							if tempWord != word:
								relatedWords.append(tempWord)
								wordCount += 1
							else:
								pass
						else:
							pass
	except:
		try:
			# print("B2 == B")
			# Source 2
			urlBase = "https://www.dictionary.com/browse/"
			urlSearch = urlBase + word
			page = requests.get(urlSearch)
			soup = BeautifulSoup(page.content, 'html.parser')
			ScrapedResults = soup.find_all("span", class_="luna-runon bold")
			for span in ScrapedResults:
				tempWord = span.text
				tempWord = regex.sub("", tempWord)
				tempWord = tempWord.strip()
				if wordCount < 10:
					if tempWord not in relatedWords:
						if tempWord != word:
							relatedWords.append(tempWord)
							wordCount += 1
						else:
							pass
		except:
			relatedWords = []
	relatedWords.sort()
	return relatedWords

# --------------------------------------------

'''
word = "communication"
print("-----------")
relatedWords = getRelatedWords(word)
relatedWords.sort()
print(word, str(len(relatedWords)))
print("-----------")
print(relatedWords)
'''