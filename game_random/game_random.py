from flask import Blueprint, current_app, render_template
import random

# NOT using pokebase in the end, the performances are so badm it takes 3-5 sec to get the object though calling the URL + parsing the json is < 250ms
#import pokebase
#use my poor man reimplementation with cache
from poorman_pokeapi_client import Pokepoor
import poorman_textutils
from config import myconfig


random_bp = Blueprint('random_bp', __name__)


@random_bp.route('/randomPokemon')
def randomPokemonPage():
    pokeid = random.randrange(1,myconfig["max pokemon id"])
    pokemon = Pokepoor.getPokemon(pokeid)
    
    desc= str(pokemon)

    if myconfig["Show stats"]:
        #DBG check the cache
        print(Pokepoor.getPokemon.cache_info())

    return render_template("template01.html", pagename="Random!", pagecontent=desc.replace('\n', '\n<br/>'), logo= pokemon.spriteURL if pokemon.spriteURL_big == "" else pokemon.spriteURL_big, **current_app.global_render_template_params)



def htmlRenderPageHeader():
    return """<td><a href="randomPokemon">Au hasard</a></td>"""

def htmlRenderHomepageCard():
    return """
<td>
    <span class="gamename"><a href="randomPokemon">Au hasard</a></span><br/>
    Les details d'un pokemon au hasard.
</td>
"""

#at last some injection of methods in the blueprint
random_bp.htmlRenderPageHeader = htmlRenderPageHeader
random_bp.htmlRenderHomepageCard = htmlRenderHomepageCard