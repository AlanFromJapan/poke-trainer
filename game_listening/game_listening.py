from flask import Blueprint, request, render_template
import random
import re

from config import myconfig

from poorman_textutils import removeAccents

listening_bp = Blueprint('listening_bp', __name__, template_folder='templates')


#ignore the possible leading "aaaaa|" and other keeps what's between double brackets [[ ]] (2nd group)
# https://pythex.org/ <3
REGEX= """\[\[([^|\]]+\|)?([^\]]+)\]\]"""

r = re.compile(REGEX)
wordlist = []

#load the file
with open("game_listening/wikisource.txt", mode="r") as f:
    wikisource = f.read()
    l = r.findall(wikisource)
    #l is a list of string tuples, we want the 2nd element of each tuple
    wordlist = [x[1] for x in l]


@listening_bp.route('/listening')
def randomWordPage():
    w = get_random_word()
    
    #I don't have a keyboard with accents, so I remove them
    w = removeAccents(w)

    #this will deserve be improved if we want to support more languages
    lang = "fr-fr" if myconfig["language"] == "fr" else "ja-jp" if myconfig["language"] == "jp" else "ko-kr"
    
    return render_template("listening_template.html", pokename=w, jscontent=f"speech2textAPI('{lang}', '{w}');" )



def get_random_word():
    return wordlist[random.randint(0, len(wordlist)-1)]