from flask import Blueprint, request, render_template, current_app, session
import random

# NOT using pokebase in the end, the performances are so badm it takes 3-5 sec to get the object though calling the URL + parsing the json is < 250ms
#import pokebase
#use my poor man reimplementation with cache
from poorman_pokeapi_client import Pokepoor
import poorman_textutils
from config import myconfig
from score_manager import score_manager


initiale_bp = Blueprint('initiale_bp', __name__, template_folder='templates')


@initiale_bp.route("/gameA")
def gameApage():
    class Card:
        letter = "?"
        def __init__(self, l) -> None:
            self.letter = l

    pokeid = random.randrange(1,myconfig["max pokemon id"])
    pokemon = Pokepoor.getPokemon(pokeid)
    name = pokemon.translations[session['language']]


    cards = []
    cards.append(name[0])
    while len(cards) < myconfig["gameA cards"]:
        l = poorman_textutils.getRandomLetter(session['language'])
        if not l in cards:
            cards.append(l)
    
    cards = [Card(x) for x in cards]

    #gotta love Python <3
    random.shuffle(cards)

    if "lastscore" in request.args:
        #inc score if we come back to this page
        current_app.global_render_template_params["scoremgr"].inc_score("gameA")
    else:
        #set initial score if we come here for the first time 
        current_app.global_render_template_params["scoremgr"].set_score("gameA", 0)


    return render_template("gameA.html", pagecontent="test test", cards=cards, letterstyle= session['letterstyle'], lettercase= session['lettercase'], pokemon=pokemon, pokename=name, **current_app.global_render_template_params)


def htmlRenderPageHeader():
    return """<td><a href="gameA">Jeu: Initiale</a></td>"""

def htmlRenderHomepageCard():
    return """
<td>
    <span class="gamename"><a href="gameA">Initiale</a></span><br/>
            Trouve la premiere lettre du nom d'un pokemon!
</td>
"""
#at last some injection of methods in the blueprint
initiale_bp.htmlRenderPageHeader = htmlRenderPageHeader
initiale_bp.htmlRenderHomepageCard = htmlRenderHomepageCard