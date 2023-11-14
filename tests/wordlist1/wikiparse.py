import os
import re
import random

#ignore the possible training "aaaaa|" and other keeps what's between double brackets [[ ]] (2nd group)
# https://pythex.org/ <3
REGEX= """\[\[([^|\]]+\|)?([^\]]+)\]\]"""

r = re.compile(REGEX)
wordlist = []
with open("wikisource.txt", mode="r") as f:
    wikisource = f.read()
    l = r.findall(wikisource)
    #l is a list of string tuples, we want the 2nd element of each tuple
    wordlist = [x[1] for x in l]


def get_random_word():
    return wordlist[random.randint(0, len(wordlist)-1)]


#now to get the image
# https://pixabay.com/api/docs/#api_javascript_example
# https://pixabay.com/api/?key=API_KEY&q=yellow+flowers&image_type=photo

# https://unsplash.com/documentation
