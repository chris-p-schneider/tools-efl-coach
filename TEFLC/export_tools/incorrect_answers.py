# ----------------------------------------
# incorrect_answers.py
# Generate Incorrect Answers for questions by type
# ----------------------------------------

# Imports
import sys
from datamuse import datamuse
import eng_to_ipa as ipa
from pysyllables import get_syllable_count

# print(sys.path)

# My Files
# ...

# ----------------------------------------

api = datamuse.Datamuse()
word = "culture"
nl = "----------------------------"

# ----------------------------------------
'''
# 1: IPA
def incorrect_ipa(correct_word, number_incorrect):

	incorrect_words = []
	# Datamuse: Spelled Like
	incorrect_results = api.words(sp=correct_word, 
								max=number_incorrect+1)

	for incorrect in incorrect_results:
		# print(incorrect["word"])
		if len(incorrect_words) < number_incorrect:
			if incorrect["word"] != correct_word:
				incorrect_word_ipa = ipa.jonvert(incorrect["word"])
				incorrect_words.append(incorrect_word_ipa)

	# If not enough results...
	if len(incorrect_words) < number_incorrect:
		# Datamuse: Sounds Like
		incorrect_results = api.words(sl=correct_word, 
									max=number_incorrect+1)
		for incorrect in incorrect_results:
			# print(incorrect["word"])
			if len(incorrect_words) < number_incorrect:
				if incorrect["word"] != correct_word:
					incorrect_word_ipa = ipa.jonvert(incorrect["word"])
					incorrect_words.append(incorrect_word_ipa)


	return incorrect_words

print(nl)
print("Which is the IPA spelling of \"{}\"?".format(word))
print("Answer:", ipa.jonvert(word))
print("Options:", incorrect_ipa(word, 3))
print(nl)

# ----------------------------------------

# 2: Type (Part of Speeech)

# ----------------------------------------

# 3: Definition [Default]

# ----------------------------------------

# 4: Syllables
def incorrect_syllables(correct_word, number_incorrect):

	incorrect_syllables = []
	correct_syllables = get_syllable_count(correct_word)
	if correct_syllables == 1:
		incorrect_syllables = [2, 3, 4]
	else:
		incorrect_syllables = [correct_syllables-1, correct_syllables+1, correct_syllables+2]

	return incorrect_syllables

print("How many syllables does \"{}\" have?".format(word))
print("Answer:", get_syllable_count(word))
print("Options:", incorrect_syllables(word, 3))
print(nl)


# ----------------------------------------
'''
# 5: Synonyms
def incorrect_synonyms(correct_word, number_incorrect):

	incorrect_synonyms = []
	correct_synonyms = api.words(rel_syn=correct_word, 
								max=25)
	# print(correct_synonyms)
	# antonym, tangentially related, or related word from list
	word_antonyms = api.words(rel_ant=correct_word, 
								max=number_incorrect+1)
	# print(word_antonyms)

	print(nl)
	print("jja", api.words(rel_jja=correct_word, 
								max=25))
	print(nl)
	print("jjb", api.words(rel_jjb=correct_word, 
								max=25))
	print(nl)
	print("trg", api.words(rel_trg=correct_word, 
								max=25))
	print(nl)
	print("spc", api.words(rel_spc=correct_word, 
								max=25))
	print(nl)
	print("gen", api.words(rel_gen=correct_word, 
								max=25))
	print(nl)


print("Which is a synonym of \"{}\"?".format(word))
# print("Answer:", )
print("Options:", incorrect_synonyms(word, 3))
print(nl)


# ----------------------------------------

# 6: Antonyms

# ----------------------------------------

# 7: Rhymes

# ----------------------------------------
