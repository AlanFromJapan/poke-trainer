import re
import unidecode

#this is NOT the first syllabe. It's something like the begining of the word until you reach the first vowel (or 2nd if it started by a vowel)
REGEX_FIRST_SYLLABISH="^\w[^aiueoy]?[aiueoy]*"

reFirstSyllabish = re.compile(REGEX_FIRST_SYLLABISH)

#Quick way to return first "syllabe" of a word
def firstSyllabish(word:str)->str:
    return reFirstSyllabish.match(word.lower()).group()

#remove accentuated characters from the string 
def removeAccents(word:str) -> str:
    return unidecode.unidecode(word)


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