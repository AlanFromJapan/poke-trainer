from flask import Blueprint, render_template, current_app, session
import random

# NOT using pokebase in the end, the performances are so badm it takes 3-5 sec to get the object though calling the URL + parsing the json is < 250ms
#import pokebase
#use my poor man reimplementation with cache
from poorman_pokeapi_client import Pokepoor
import poorman_textutils
from config import myconfig


initiale_bp = Blueprint('initiale_bp', __name__, template_folder='templates')


@initiale_bp.route("/initiale")
def game_initiale():
    class Card:
        def __init__(self, l) -> None:
            self.letter = l

    pokeid = random.randrange(1,myconfig["max pokemon id"])
    pokemon = Pokepoor.getPokemon(pokeid)
    name = pokemon.translations[session['language']]


    cards = []
    cards.append(name[0])
    while len(cards) < myconfig["gameA cards"]:
        l = poorman_textutils.getRandomLetter(session['language'])
        if l not in cards:
            cards.append(l)
    
    cards = [Card(x) for x in cards]

    #gotta love Python <3
    random.shuffle(cards)

    return render_template("gameA.html", cards=cards, pokemon=pokemon, pokename=name, **current_app.global_render_template_params)


def htmlRenderPageHeader():
    return """<td><a href="initiale">Jeu: Initiale</a></td>"""

def htmlRenderHomepageCard():
    return """
<td>
    <span class="gamename"><a href="initiale">Initiale</a></span><br/>
            Trouve la premiere lettre du nom d'un pokemon!
</td>
"""
#at last some injection of methods in the blueprint
initiale_bp.htmlRenderPageHeader = htmlRenderPageHeader
initiale_bp.htmlRenderHomepageCard = htmlRenderHomepageCard