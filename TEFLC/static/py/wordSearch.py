# wordSearch.py
# Wordsearch Generator

# Inputs: wordList, x, y
# Output: wordSearchList

# IMPORTS ///////////////////////////////////////////////////////////////
import sys
import random
import numpy as np

# GLOBAL CONSTANTS //////////////////////////////////////////////////////
# example list
vocabList = ["awesome", "orange", "banana", "pear", 
			"peach", "avocado", "coconut", "cherry"]
# copy & to upper
wordList = ""

# The Default Wordsearch Size: (16, 13)
x = 16
y = 13

newLine = ""
for c in range (x+(x-1)):
	newLine = newLine + "-"

# A dictionary template for each coordinate's info
coordsDictDefault = {
	"Number": 0, "Character": '-', "nType": '-', "X": 0, "Y": 0 
	}
# The master dictionary that will contain all the Wordsearch grid data
coordsDict = {}

# reference dictionary of directions
directionsDictReference = {
	'1': "U", '2': "RU", '3': "R", '4': "RD",
	'5': "D", '6': "LD", '7': "L", '8': "LU"
	}
# direction edge checking dictionary, uses string[0,1] for two checks
directionEdgeDictReference = {
	1: 'TT', 2: 'TR', 3: 'RR', 4: 'RB', 5: 'BB', 6: 'BL', 7: 'LL', 8: 'TL'
	}


# FUNCTION LIST /////////////////////////////////////////////////////////

# converts vocabList to uppercase
def upperWords (vocabList):
	vocabList = [element.upper() for element in vocabList]
	return vocabList

# determines longest word in list and total characters of all words in list
def wordChars (vocabList):
	longestWord = 0
	totalWordChars = 0
	wordCharsCounter = 0
	while wordCharsCounter < len(vocabList):
		totalWordChars = (totalWordChars + len(vocabList[wordCharsCounter])) 
		if len(vocabList[wordCharsCounter]) > longestWord:
			longestWord = len(vocabList[wordCharsCounter])
		wordCharsCounter += 1
	return longestWord, totalWordChars

# checks that grid will fit words: x|y > len(longestWord) && xy > charCount*2
def defineGrid (longestAndTotal, x, y):
	print (longestAndTotal)
	print ("x: " + str(x))
	print ("y: " + str(y))
	if longestAndTotal[0] > (x or y):
		sys.exit ("Your longest word won't fit in this Wordsearch!")
	elif (x*y) > (longestAndTotal[1]*2):
		pass
	else:
		print ("The ratio of word characters to grid coordinates is: " 
			+ str(longestAndTotal[1]) + ":" + str(x*y))
		print ("That leaves " + str((x*y)-(longestAndTotal[1])) + " filler spaces.")
		print ("I think " + str((longestAndTotal[1]*2)) + " is a reasonable minimum area.")
		sys.exit ("Your grid size of " + str(x*y) + " is too small for the word list!")


# creates a dictionary of each numbered coordinate in the grid (1:xy)
# each coordinate is a dictionary with default values: (#:0, C='-', x=0, y=0)
def defineCoords (coordsDictDefault, x, y):
	coordsDict = {}
	defineCoordsCounter = 1
	xCounter = 1
	yCounter = 1
	while defineCoordsCounter < ((x*y)+1):
		foundCoord = False
		while foundCoord == False:
			temporaryDict = coordsDictDefault.copy()
			temporaryDict["Number"] = defineCoordsCounter
			temporaryDict["Character"] = '-'
			temporaryDict["nType"] = '-'
			if xCounter < (x+1):
				temporaryDict["X"] = xCounter
				temporaryDict["Y"] = yCounter
				coordsDict[defineCoordsCounter] = temporaryDict
				foundCoord = True
			elif xCounter == ((x*yCounter)+1):
				xCounter = 0
				yCounter += 1
			xCounter += 1
		defineCoordsCounter += 1
	return coordsDict

# determines if a coordinate number is a corner (Left Right Top Bottom)
def checkCorner (n, x, y):
	if n == 1:
		nType = "LT"
	elif n == x:
		nType = "RT"
	elif n == (x*y):
		nType = "RB"
	elif n == ((x*y)-(x-1)):
		nType = "LB"
	else: 
		nType ="-"
	return nType

# determines if a coordinate number is an edge (Top Right Bottom Left) or Middle
def checkEdge (n, coordsDict, x, y):
	if n < (x+1):
		nType = "T"
	elif (n%x) == 0:
		nType = "R"
	elif n > ((x*y)-x):
		nType = "B" 
	elif coordsDict.get(n).get('X') == 1:
		nType = "L"
	else:
		nType = "M"
	return nType

# determine if corner, edge, or middle
# used in updateDictCECounter and applied to all coords
def checkDirection (n, coordsDict, x, y):
	temporaryNType = coordsDict.get(n).get('nType')
	temporaryNType = checkCorner (n, x, y)
	if temporaryNType == '-':
		temporaryNType = checkEdge (n, coordsDict, x, y)
	return temporaryNType

# updates coordsDict with nType for each coordinate
def updateDictCE (coordsDict, x, y):
	updateDictCECounter = 1
	while updateDictCECounter < ((x*y)+1):
		coordsDict[updateDictCECounter]['nType'] = checkDirection (updateDictCECounter, coordsDict, x, y)
		updateDictCECounter += 1

# returns value of direction from given coordinate
# "goes" (direction) one step to next coordinate
# used to iterate the unvalidated direction in getDirections
def goDirection (n, i, x):
	directions = {
		1: lambda U: n-x,
		2: lambda RU: n-(x-1),
		3: lambda R: n+1,
		4: lambda RD: n+(x+1),
		5: lambda D: n+x,
		6: lambda LD: n+(x-1),
		7: lambda L: n-1,
		8: lambda LU: n-(x+1),
		}
	return directions.get(i)(n)


# checks all 8 directions for n and returns unvalidated direction list
# the list shows the coordinate in the given direction
# used in validateDirectionList to produced validated list
def getDirections (n, x):
	unvalidatedDirectionList = []
	getDirectionsCounter = 1
	while getDirectionsCounter < 9:
		currentDirection = goDirection (n, getDirectionsCounter, x)
		unvalidatedDirectionList.append(currentDirection)
		getDirectionsCounter += 1
	return unvalidatedDirectionList

# checks if corner or edge and sets out of bounds direction to 0
# returns the validateDirectionList which is used to check distance
def validateDirectionList (n, nType, directionList, coordsDict):
	if coordsDict[n]['nType'] == "LT":
		directionList[0] = 0
		directionList[1] = 0
		directionList[5] = 0
		directionList[6] = 0
		directionList[7] = 0
	elif coordsDict[n]['nType'] == "RT":
		directionList[0] = 0
		directionList[1] = 0
		directionList[2] = 0
		directionList[3] = 0
		directionList[7] = 0
	elif coordsDict[n]['nType'] == "RB":
		directionList[1] = 0
		directionList[2] = 0
		directionList[3] = 0
		directionList[4] = 0
		directionList[5] = 0
	elif coordsDict[n]['nType'] == "LB":
		directionList[3] = 0
		directionList[4] = 0
		directionList[5] = 0
		directionList[6] = 0
		directionList[7] = 0
	elif coordsDict[n]['nType'] == "T":
		directionList[0] = 0
		directionList[1] = 0
		directionList[7] = 0
	elif coordsDict[n]['nType'] == "R":
		directionList[1] = 0
		directionList[2] = 0
		directionList[3] = 0
	elif coordsDict[n]['nType'] == "B":
		directionList[3] = 0
		directionList[4] = 0
		directionList[5] = 0
	elif coordsDict[n]['nType'] == "L":
		directionList[5] = 0
		directionList[6] = 0
		directionList[7] = 0
	return directionList


# takes validated direction list and iterates onward from each new direction
# considers if character in grid matches current letter of current word
# returns a list of values of maximum distance per direction
# this could have been done more elegantly but it works so oh well
def measureDistance (coordsDict, validateDirectionList, currentWord, x):
	finalDistancesList = validateDirectionList.copy()
	findDistancesCounter = 0
	while findDistancesCounter < 8:
		temporaryDistance = 0
		if validateDirectionList[findDistancesCounter] > 0:
			temporaryDistance = 2
			nextDirection = validateDirectionList[findDistancesCounter]
			if coordsDict[nextDirection]['Character'] != '-':
				if coordsDict[nextDirection]['Character'] == currentWord[1]:
					pass
				else:
					temporaryDistance = 1
					finalDistancesList[findDistancesCounter] = temporaryDistance
					findDistancesCounter += 1
					continue
			if directionEdgeDictReference[(findDistancesCounter+1)][0] in coordsDict[validateDirectionList[findDistancesCounter]]['nType']:
				pass
			elif directionEdgeDictReference[(findDistancesCounter+1)][1] in coordsDict[validateDirectionList[findDistancesCounter]]['nType']:
				pass
			else: 	
				currentWordDistanceCounter = 2 # one direction from initial == index 1 + next?
				while nextDirection > 0:
					nextDirection = goDirection(nextDirection, (findDistancesCounter+1), x)
					if nextDirection < 1:
						break
					elif coordsDict[nextDirection]['Character'] != '-':
						if coordsDict[nextDirection]['Character'] == currentWord[currentWordDistanceCounter]:
							if directionEdgeDictReference[(findDistancesCounter+1)][0] in coordsDict[nextDirection]['nType']:
								temporaryDistance += 1
								nextDirection = 0
							elif directionEdgeDictReference[(findDistancesCounter+1)][1] in coordsDict[nextDirection]['nType']:
								temporaryDistance += 1
								nextDirection = 0
							else:
								temporaryDistance += 1
						else:
							temporaryDistance = 2
							break
					elif directionEdgeDictReference[(findDistancesCounter+1)][0] in coordsDict[nextDirection]['nType']:
						temporaryDistance += 1
						nextDirection = 0
					elif directionEdgeDictReference[(findDistancesCounter+1)][1] in coordsDict[nextDirection]['nType']:
						temporaryDistance += 1
						nextDirection = 0
					else:
						temporaryDistance += 1
					if currentWordDistanceCounter < (len(currentWord)-1):
						currentWordDistanceCounter += 1
		finalDistancesList[findDistancesCounter] = temporaryDistance
		findDistancesCounter += 1
	return finalDistancesList

# Chooses direction using distances > directional coordinates
# direction determined by location in list, returns list index value
def chooseDirection (distancesList, currentWord):
	directionValid = False
	while directionValid == False:
		randomDirection = random.randint(0, (len(distancesList)-1))
		if distancesList[randomDirection] >= len(currentWord):
			directionValid = True
	return randomDirection

# places each character on grid if space free
def placeCharacter (initialCoord, currentWord, seedDirection, directionList, coordsDict, x, y):
	placeCharacterCounter = 0
	placeCharacterDirectionsList = directionList
	placeCharacterWhere = initialCoord
	while (placeCharacterCounter < len(currentWord)):
		coordsDict[placeCharacterWhere]['Character'] = currentWord[placeCharacterCounter]
		placeCharacterWhere = goDirection (placeCharacterWhere, (seedDirection+1), x)
		placeCharacterDirectionsList = getDirections (placeCharacterWhere, x)
		if placeCharacterWhere < ((x * y)+1) and placeCharacterWhere > 0:
			placeCharacterDirectionsList = validateDirectionList (placeCharacterWhere, 
				coordsDict[placeCharacterWhere]['nType'], placeCharacterDirectionsList, coordsDict)
		placeCharacterCounter += 1

# chooses random initial coodinate within grid range
# measures distances using current word current char to check grid chars
# after determining possible directions (minDist < dist), chooses randomly
# validates that dir dist > len(word)
# places word char by char via direction, updating char dict per placement
def placeWord (currentWord, coordsDict, x, y):
	minDist = len(currentWord)
	validInitialCoord = False
	while validInitialCoord == False:
		initalCoordUnoccupied = False
		while initalCoordUnoccupied == False:
			initialCoord = random.randint(1, (x*y))
			if coordsDict[initialCoord]['Character'] == '-':
				initalCoordUnoccupied = True
		directionsList = getDirections (initialCoord, x) 
		directionsList = validateDirectionList (initialCoord, 
			coordsDict[initialCoord]['nType'], 
			directionsList, coordsDict)
		distancesList = measureDistance (coordsDict, directionsList, currentWord, x)
		checkInitialCounter = 0
		distanceValidator = 0
		while checkInitialCounter < len(distancesList):
			distanceValidator = distancesList[checkInitialCounter]
			if distanceValidator >= minDist:
				validInitialCoord = True
			checkInitialCounter += 1
	seedDirection = chooseDirection (distancesList, currentWord)
	placeCharacter (initialCoord, currentWord, seedDirection, directionsList, coordsDict, x, y)

# creates array of coordinates from 1 to (x*y) and returns array list
def makeCoordsArray (x, y):
	arrayList = []
	rowList = []
	rowCounter = 1
	arrayCounter = 1
	while arrayCounter < ((x*y)+1):
		while arrayCounter < ((x*rowCounter)+1):
			rowList.append (arrayCounter)
			arrayCounter += 1
		arrayList.append (rowList)
		rowList = []
		rowCounter += 1
	return arrayList

# creates new array of chars using coordsDict, returns array of chars
def makeCharArray (coordsDict, x, y):
	charArrayList = []
	charRowList = []
	charCounter = 1
	charRowCounter = 1
	while charCounter < ((x*y)+1):
		while charCounter < ((x*charRowCounter)+1):
			charRowList.append (coordsDict[charCounter]['Character'])
			charCounter += 1
		charArrayList.append (charRowList)
		charRowList = []
		charRowCounter += 1
	return charArrayList

# takes in string of array, removes array formatting and outputs clean string
def formatArray (strArray):
	delimitersToRemove = ['[', '\'', ']', ' ']
	reformatSpaces = '|'
	for ele in strArray:
		if ele in delimitersToRemove:
			strArray = strArray.replace(ele, "")
	for ele in strArray:
		if ele in reformatSpaces:
			strArray = strArray.replace(ele, ' ')
	if "  \n" in strArray:
		strArray = strArray.replace("  \n", "\n")
	return strArray
	
# prints arrays for inspection, returns character array for assignment
def printArrays (coordsDict, x, y):
	charArrayList = makeCharArray (coordsDict, x, y)
	charArray = np.array(charArrayList)
	strCharArray =  np.array2string(charArray, separator="||")
	strCharArray = formatArray (strCharArray)
	print (strCharArray)
	print (charArray)
	print (newLine)
	return strCharArray

# fills the remaining space on the grid with random characters
# character reference file uses English letter by actual frequency
def fillSpace (coordsDict, x, y):
	fillSpaceTxt = open ('fillSpace.txt', 'r')
	fillSpaceChars = fillSpaceTxt.read()
	for key in coordsDict.keys():
		if coordsDict[key]['Character'] == '-':
			randomCharIndex = random.randint(0,993)
			randomChar = fillSpaceChars[randomCharIndex]
			coordsDict[key]['Character'] = randomChar


# MAIN EXECUTION ////////////////////////////////////////////////////////
def generateWordSearch (vocabList, x, y): 
	wordList = upperWords(vocabList)
	longestAndTotal = wordChars(vocabList)
	defineGrid (longestAndTotal, x, y)
	coordsDict = defineCoords (coordsDictDefault, x, y)
	updateDictCE (coordsDict, x, y)
	placeWordCounter = 0
	while placeWordCounter < len(wordList):
		placeWord (wordList[placeWordCounter], coordsDict, x, y)
		placeWordCounter += 1
	print (newLine)
	print ("Answer Key: ")
	print (newLine)
	answerKey = printArrays (coordsDict, x, y)
	fillSpace (coordsDict, x, y)
	print ("Word Search: ")
	print (newLine)
	wordSearch = printArrays (coordsDict, x, y)
	wordSearchList = wordSearch.rsplit('\n')
	return wordSearchList

wordSearchList = generateWordSearch (vocabList, x, y)