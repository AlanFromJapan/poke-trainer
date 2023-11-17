from flask import Blueprint, request, render_template
import random

# NOT using pokebase in the end, the performances are so badm it takes 3-5 sec to get the object though calling the URL + parsing the json is < 250ms
#import pokebase
#use my poor man reimplementation with cache
from poorman_pokeapi_client import Pokepoor
import poorman_textutils
from config import myconfig


melimelo_bp = Blueprint('melimelo_bp', __name__, template_folder='templates')


@melimelo_bp.route("/gameC")
def gameCpage():
    score = 0
    pokeid = random.randrange(1,myconfig["max pokemon id"])
    pokemon = Pokepoor.getPokemon(pokeid)
    name = pokemon.translations[myconfig['language']]

    if myconfig['language'] == "fr":
        #remove nasty accents
        name = poorman_textutils.removeAccents(name)

    
    score = int(request.args.get('lastscore', default="-1")) + 1   

    return render_template("gameC.html", pagecontent="test test", score=score, pokemon=pokemon, pokename=name)


def htmlRenderPageHeader():
    return """<td><a href="listening">Jeu: Meli-melo</a></td>"""

def htmlRenderHomepageCard():
    return """
<td>
    <span class="gamename">Meli-melo</span><br/>
        Remet les lettres dans le bon ordre.
</td>
"""
#at last some injection of methods in the blueprint
melimelo_bp.htmlRenderPageHeader = htmlRenderPageHeader
melimelo_bp.htmlRenderHomepageCard = htmlRenderHomepageCard