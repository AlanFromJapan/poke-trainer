from flask import Blueprint, request, render_template, current_app
import random

# NOT using pokebase in the end, the performances are so badm it takes 3-5 sec to get the object though calling the URL + parsing the json is < 250ms
#import pokebase
#use my poor man reimplementation with cache
from poorman_pokeapi_client import Pokepoor
import poorman_textutils
from config import myconfig


pendu_bp = Blueprint('pendu_bp', __name__, template_folder='templates')


@pendu_bp.route("/gameB")
def gameBpage():
    score = 0
    pokeid = random.randrange(1,myconfig["max pokemon id"])
    pokemon = Pokepoor.getPokemon(pokeid)
    name = pokemon.translations[myconfig['language']]

    if myconfig['language'] == "fr":
        #remove nasty accents
        name = poorman_textutils.removeAccents(name)

    
    score = int(request.args.get('lastscore', default="-1")) + 1   

    return render_template("gameB.html", pagecontent="test test", score=score, pokemon=pokemon, pokename=name, **current_app.global_render_template_params)


def htmlRenderPageHeader():
    return """<td><a href="gameB">Jeu: Pendu</a></td>"""

def htmlRenderHomepageCard():
    return """
<td>
    <span class="gamename"><a href="gameB">Pendu</a></span><br/>
            Le jeu du pendu, ecrit tout le mot sans te tromper sinon...
</td>
"""
#at last some injection of methods in the blueprint
pendu_bp.htmlRenderPageHeader = htmlRenderPageHeader
pendu_bp.htmlRenderHomepageCard = htmlRenderHomepageCard