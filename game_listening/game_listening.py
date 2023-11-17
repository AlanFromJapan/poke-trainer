from flask import Blueprint, request, render_template
import random
import re

from config import myconfig

from LanguageItem import LanguageItem
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
    toHear = get_random_word()
    
    #I don't have a keyboard with accents, so I remove them
    toType = removeAccents(toHear)

    la = LanguageItem(toType, toHear, None, myconfig["language"])

    return render_template("listening_template.html", item=la)


def htmlRenderPageHeader():
    return """<td><a href="listening">Jeu: Ecoute</a></td>"""

def htmlRenderHomepageCard():
    return """
<td>
    <span class="gamename"><a href="listening">Jeu: Ecoute</a></span><br/>
    Ecoute un mot et tape le mot entendu.
</td>
"""



def get_random_word():
    return wordlist[random.randint(0, len(wordlist)-1)]

#at last some injection of methods in the blueprint
listening_bp.htmlRenderPageHeader = htmlRenderPageHeader
listening_bp.htmlRenderHomepageCard = htmlRenderHomepageCard