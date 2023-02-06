from flask import Flask, render_template, redirect, url_for, request, make_response, send_file
import os, sys
import logging
from logging.handlers import RotatingFileHandler
import re
import werkzeug 
import pokebase
import random

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
    return render_template("home01.html", pagename="Home", logo= pokebase.SpriteResource('pokemon', random.randrange(1, 150)).url)


@app.route('/randomPokemon')
def randomPokemonPage():
    pokeid = random.randrange(1,150)
    pokemon= pokebase.pokemon(pokeid)
    specie=pokebase.pokemon_species(pokeid)
    
    desc= f"""
Name :  {pokemon.name}
ID:     {pokemon.id}
url:    {pokemon.url}
types:  {pokemon.types}
species:{pokemon.species}
sprites:<img src="{pokemon.sprites.front_default}" />    
"""
    print(desc)

    spe=f"""
Name:   {specie.name}
Fr:     {specie.names[4].name}    
    """
    print(spe)

    return render_template("template01.html", pagename="Random!", pagecontent=(desc + spe).replace('\n', '\n<br/>'), logo= pokebase.SpriteResource('pokemon', pokeid).url)




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