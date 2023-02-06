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


########################################################################################
## Flask vars
#
app = Flask(__name__, static_url_path='')

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
    return render_template("home01.html", pagename="Home", logo= Pokepoor.getPokemon(random.randrange(1, 150)).spriteURL)


@app.route('/randomPokemon')
def randomPokemonPage():
    pokeid = random.randrange(1,150)
    pokemon = Pokepoor.getPokemon(pokeid)
    
    desc= f"""
Name :  {pokemon.name}
ID:     {pokemon.id}
species:{pokemon.species}
sprites:<img src="{pokemon.spriteURL}" />    
"""
    print(desc)

    spe=f"""
Name:   {pokemon.species}
Fr:     {pokemon.translations["fr"]}    
    """
    print(spe)

    return render_template("template01.html", pagename="Random!", pagecontent=(desc + spe).replace('\n', '\n<br/>'), logo= pokemon.spriteURL)




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