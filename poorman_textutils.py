import re
import unidecode
import random

#this is NOT the first syllabe. It's something like the begining of the word until you reach the first vowel (or 2nd if it started by a vowel)
REGEX_FIRST_SYLLABISH="^\w[^aiueoy]?[aiueoy]*"

reFirstSyllabish = re.compile(REGEX_FIRST_SYLLABISH)

#Quick way to return first "syllabe" of a word
def firstSyllabish(word:str)->str:
    return reFirstSyllabish.match(word.lower()).group()

#remove accentuated characters from the string 
def removeAccents(word:str) -> str:
    return unidecode.unidecode(word)


#returns a letter in a "language" so ja => katakana, ko => hangul, the rest gets A-Z
def getRandomLetter(lang):
    if lang == "ja":
        #https://en.wikipedia.org/wiki/Katakana_(Unicode_block)
        #start at 0x30A0 (=12448)
        return chr(12448 -1 + random.randrange(1, 80))
    #if lang == "ko":
        #https://en.wikipedia.org/wiki/Hangul_Jamo_(Unicode_block)
        #start at 0x1100 (=4352)
        #TODO spli in 3 and use the composable ones only (green background)
    
    #default case: A-Z
    return chr(ord('A') -1 + random.randrange(1, 26))


#Standalone test
if __name__ == '__main__':
    print("================= STANDALONE TEST")

    tests = ["bonjour",
"alex",
"pikachu",
"raichu",
"psykokwak",
"akwakwak",
"taupiqueur",
"Électrode",
"Aéromite",
"Magnéton"]

    for test in tests:
        print(f"{test} -> [{firstSyllabish(test)}]")

    print("-----------------Text removing accents----------------")
    for test in tests:
        print(f"{test} -> [{removeAccents(test)}]")