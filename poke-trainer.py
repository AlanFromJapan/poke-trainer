from flask import Flask, render_template, redirect, url_for, request, make_response, send_file
import os, sys
import logging
from logging.handlers import RotatingFileHandler
import re
import werkzeug
import random

# NOT using pokebase in the end, the performances are so badm it takes 3-5 sec to get the object though calling the URL + parsing the json is < 250ms
#import pokebase
#use my poor man reimplementation with cache
from poorman_pokeapi_client import Pokepoor
import poorman_textutils
from config import myconfig


########################################################################################
## Flask vars
#
app = Flask(__name__, static_url_path='')
app.secret_key = myconfig["session secret key"]

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ico'])

########################################################################################
## Flask init
#
@app.before_first_request
def init():
    pass


########################################################################################
## Web related functions
#
@app.route('/')
def homepage():
    return render_template("home01.html", pagename="Home", logo= Pokepoor.getPokemon(random.randrange(1, myconfig["max pokemon id"])).spriteURL)



@app.route('/randomPokemon')
def randomPokemonPage():
    pokeid = random.randrange(1,myconfig["max pokemon id"])
    pokemon = Pokepoor.getPokemon(pokeid)
    
    desc= str(pokemon)

    return render_template("template01.html", pagename="Random!", pagecontent=desc.replace('\n', '\n<br/>'), logo= pokemon.spriteURL if pokemon.spriteURL_big == "" else pokemon.spriteURL_big)



@app.route("/gameA")
def gameApage():
    class Card:
        letter = "?"
        def __init__(self, l) -> None:
            self.letter = l

    pokeid = random.randrange(1,myconfig["max pokemon id"])
    pokemon = Pokepoor.getPokemon(pokeid)
    name = pokemon.translations[myconfig['language']]


    cards = []
    cards.append(name[0])
    while len(cards) < myconfig["gameA cards"]:
        l = chr(ord('A') -1 + random.randrange(1, 26))
        if not l in cards:
            cards.append(l)
    
    cards = [Card(x) for x in cards]

    #gotta love Python <3
    random.shuffle(cards)

    score = int(request.args.get('lastscore', default="-1")) + 1   
    
    return render_template("gameA.html", pagecontent="test test", cards=cards, pokemon=pokemon, pokename=name, score=score)



########################################################################################
## Main entry point
#
if __name__ == '__main__':
    try:
        #start web interface
        app.debug = True
        app.run(host='0.0.0.0', port=56789, threaded=True)

    finally:
        pass