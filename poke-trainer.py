from flask import Flask, render_template, redirect, url_for, request, make_response, send_file
import os, sys
import logging
from logging.handlers import RotatingFileHandler
import re
import werkzeug
import random

#running behind proxy?                                                                                            
from werkzeug.middleware.proxy_fix import ProxyFix

# NOT using pokebase in the end, the performances are so badm it takes 3-5 sec to get the object though calling the URL + parsing the json is < 250ms
#import pokebase
#use my poor man reimplementation with cache
from poorman_pokeapi_client import Pokepoor
import poorman_textutils
from config import myconfig


#Blueprints
from api.api import api_bp
from game_initale.game_initiale import initiale_bp
from game_pendu.game_pendu import pendu_bp

########################################################################################
## Flask vars
#
app = Flask(__name__, static_url_path='')
app.secret_key = myconfig["session secret key"]

#if behind a proxy set the WSGI properly 
# see http://electrogeek.tokyo/setup%20flask%20behind%20nginx%20proxy.html
if myconfig["BehindProxy"]:
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ico'])


########################################################################################
## Web related functions
#
#-----------------------------------------------------------------------
#Landing page, not much to see here but at least if API connectivity doesn't you will know immediately
@app.route('/')
def got2home():
    return redirect("/home")

@app.route('/home')
def homepage():
    return render_template("home01.html", pagename="Home", logo= Pokepoor.getPokemon(random.randrange(1, myconfig["max pokemon id"])).spriteURL)


#-----------------------------------------------------------------------
#Get a random pokemon, good for debugging
@app.route('/randomPokemon')
def randomPokemonPage():
    pokeid = random.randrange(1,myconfig["max pokemon id"])
    pokemon = Pokepoor.getPokemon(pokeid)
    
    desc= str(pokemon)

    if myconfig["Show stats"]:
        #DBG check the cache
        print(Pokepoor.getPokemon.cache_info())

    return render_template("template01.html", pagename="Random!", pagecontent=desc.replace('\n', '\n<br/>'), logo= pokemon.spriteURL if pokemon.spriteURL_big == "" else pokemon.spriteURL_big)

    
#-----------------------------------------------------------------------
#GAME A : find the initiale/first letter of a Pokemon!
app.register_blueprint(initiale_bp)
    
#-----------------------------------------------------------------------
#GAME B : pendu type of game
app.register_blueprint(pendu_bp)
    
#-----------------------------------------------------------------------
#GAME C : "meli-melo" put the letters of the pokemon in the right order
@app.route("/gameC")
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

#-----------------------------------------------------------------------
#REST API to change the language
app.register_blueprint(api_bp, url_prefix='/api')

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