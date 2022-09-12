# 9
# getRhymingWords.py

# --------------------------------------------
import requests
import datamuse
from bs4 import BeautifulSoup
import pronouncing

from TEFLC.getWordInfo.getWordSyllables import getWordSyllables # use for WordInfo.py
# from getWordSyllables import getWordSyllables # use for test
# Used to match rhyme syllables

# --------------------------------------------
api = datamuse.Datamuse()
api.set_max_default(50)

# --------------------------------------------
# Returns a list of rhyming words
# Tries 3 sources

def getRhymingWords (word):
	wordSyllables = getWordSyllables(word)
	rhymingWords = []
	rhymingWordCount = 0
	# print("A")
	# Souce 1: API
	apitest = api.words(rel_rhy=word)
	# print(apitest)
	proCheck = pronouncing.rhymes(word)
	# Check API against pronouncing package
	for result in apitest:
		tempWord = result["word"]
		tempSyllables = result["numSyllables"]
		if rhymingWordCount < 10:
			if wordSyllables >= tempSyllables >= wordSyllables-2:
				if tempWord not in rhymingWords:
					if tempWord in proCheck:
						rhymingWords.append(tempWord)
						rhymingWordCount += 1
	if rhymingWordCount < 10:
		currentLetter = ""
		formerLetter = ""
		correctSyllables = False
		try:
			# print("B")
			# Source 2
			urlBase = "https://www.rhymezone.com/r/rhyme.cgi?Word="
			urlSearch = urlBase + word + "&typeofrhyme=perfect&org1=syl&org2=l&org3=y"
			page = requests.get(urlSearch)
			soup = BeautifulSoup(page.content, 'html.parser')
			ScrapedResults = soup.find_all("b")
			# Try syllable match first
			for b in ScrapedResults:
				if correctSyllables == False:
					pass
				else:
					a = b.find("a", class_="r")
					if a:
						if rhymingWordCount < 10:
							tempWord = a.text
							tempWord = tempWord.replace(u'\xa0', u' ')
							tempWord = tempWord.strip()
							if currentLetter == "":
								formerLetter = tempWord[0]
								currentLetter = tempWord[0]
								if tempWord not in rhymingWords:
									rhymingWords.append(tempWord)
									rhymingWordCount += 1
							else:
								currentLetter = tempWord[0]
								if currentLetter == formerLetter:
									pass
								else:
									if tempWord not in rhymingWords:
										rhymingWords.append(tempWord)
										formerLetter = currentLetter
										rhymingWordCount += 1
				if "syllable" in b.text:
					if str(wordSyllables) in b.text:
						correctSyllables = True
			# Add rhymes with different syllables
			correctSyllables = False
			if rhymingWordCount < 10:
				for b in ScrapedResults:
					if correctSyllables == False:
						pass
					else:
						a = b.find("a", class_="r")
						if a:
							tempWord = a.text
							tempWord = tempWord.replace(u'\xa0', u' ')
							tempWord = tempWord.strip()
							if rhymingWordCount < 10:
								if tempWord not in rhymingWords:
									if currentLetter == "":
										formerLetter = tempWord[0]
										currentLetter = tempWord[0]
										rhymingWords.append(tempWord)
										rhymingWordCount += 1
									else:
										currentLetter = tempWord[0]
										if currentLetter == formerLetter:
											pass
										else:
											rhymingWords.append(tempWord)
											formerLetter = currentLetter
											rhymingWordCount += 1
						else:
							pass
					if "syllable" in b.text:
						correctSyllables = True
			# Add weak rhymes if not enough good rhymes
			if rhymingWordCount < 10:
				try:
					ScrapedResults2 = soup.find_all("a", class_="d r")
					tempRhyme = ""
					for result in ScrapedResults2:
						if rhymingWordCount < 10:
							if result.text not in rhymingWords:
								tempRhyme = result.text
								tempWord = tempWord.replace(u'\xa0', u' ')
								tempRhyme = tempRhyme.strip()
								rhymingWords.append(tempRhyme)
								rhymingWordCount += 1
				except:
					pass
		except:
			try:
				# print("C")
				# Source 3
				urlBase = "https://www.rhymedb.com/word/"
				urlSearch = urlBase + word
				page = requests.get(urlSearch)
				soup = BeautifulSoup(page.content, 'html.parser')
				while rhymingWordCount < 10:
					ScrapedResults1 = soup.find_all("a", class_="word syl3 top1")
					for result1 in ScrapedResults1:
						if rhymingWordCount < 10:
							tempWord = result1.text.lower()
							tempWord = tempWord.strip()
							if currentLetter == "":
								formerLetter = tempWord[0]
								currentLetter = tempWord[0]
								rhymingWords.append(tempWord)
								rhymingWordCount += 1
							else:
								currentLetter = tempWord[0]
								if currentLetter == formerLetter:
									pass
								else:
									rhymingWords.append(tempWord)
									formerLetter = currentLetter
									rhymingWordCount += 1
					# Add weak rhymes if not enough strong rhymes
					ScrapedResults2 = soup.find_all("a", class_="word syl3 top2")
					for result2 in ScrapedResults2:
						if rhymingWordCount < 10:
							tempWord = result2.text.lower()
							tempWord = tempWord.strip()
							if currentLetter == "":
								formerLetter = tempWord[0]
								currentLetter = tempWord[0]
								rhymingWords.append(tempWord)
								rhymingWordCount += 1
							else:
								currentLetter = tempWord[0]
								if currentLetter == formerLetter:
									pass
								else:
									rhymingWords.append(tempWord)
									formerLetter = currentLetter
									rhymingWordCount += 1
			except:
				pass

	rhymingWords.sort()
	return rhymingWords

# --------------------------------------------

'''
word = "nice"
wordSyllables = getWordSyllables(word)
# print(wordSyllables)
rhymingWords = getRhymingWords(word)

print(word, str(len(rhymingWords)))
print("--------------")
print(rhymingWords)
print("--------------")
'''