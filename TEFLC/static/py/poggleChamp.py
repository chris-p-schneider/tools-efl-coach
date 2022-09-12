# poggleChamp.py
# Boggle Clone

import random

'''
Original, New:
AACIOT	AAEEGN
ABILTY	ABBJOO
ABJMOQu	ACHOPS
ACDEMP	AFFKPS
ACELRS	AOOTTW
ADENVZ	CIMOTU
AHMORS	DEILRX
BIFORX	DELRVY
DENOSW	DISTTY
DKNOTU	EEGHNW
EEFHIY	EEINSU
EGKLUY	EHRTVW
EGINTV	EIOSST
EHINPS	ELRTTY
ELPSTU	HIMNUQu
GILRUW	HLNNRZ
'''

# Define Poggle Dictionary of Dice
poggleDict = {
	1: "AAEEGN",
	2: "ABBJOO",
	3: "ACHOPS",
	4: "AFFKPS",
	5: "AOOTTW",
	6: "CIMOTU",
	7: "DEILRX",
	8: "DELRVY",
	9: "DISTTY",
	10: "EEGHNW",
	11: "EEINSU",
	12: "EHRTVW",
	13: "EIOSST",
	14: "ELRTTY",
	15: "HIMNUQ", #u
	16: "HLNNRZ"
}

# Generate Gamestate String
poggleList = []
for x in range (1, 17):
	poggleList.append(poggleDict[x][random.randrange(0,len(poggleDict[x]))])

# Replace Q with Qu if present
poggleList = [char.replace('Q', "Qu") for char in poggleList]
random.shuffle(poggleList)

# Game Display
print("\n--------------------")
print("----POGGLE-CHAMP----")
print("--------------------")

# Print within List
print(poggleList[0:4])
print(poggleList[4:8])
print(poggleList[8:12])
print(poggleList[12:16])
print("--------------------")
print("--------------------\n")

'''
# Convert to Strings
poggleRow1 = " | ".join(poggleList[0:4])
poggleRow2 = " | ".join(poggleList[4:8])
poggleRow3 = " | ".join(poggleList[8:12])
poggleRow4 = " | ".join(poggleList[12:16])

# Game Display 2
print("-----------------")
print("--Poggle--Champ--")
print("-----------------")
print('| '+poggleRow1+' |')
print('| '+poggleRow2+' |')
print('| '+poggleRow3+' |')
print('| '+poggleRow4+' |')
print("-----------------")
print("-----------------")
'''

# Solve Possible Words:
# - Length Range 2:17 Maximum
# - Reasonable Length 2:8
# - Identify vocabulary word count
# - Show solutions -> Visually?
# - Show maximum points
# - Maybe allow clicking the found answers to quick add points?
# ?