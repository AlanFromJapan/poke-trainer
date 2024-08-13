import random
import logging
import os

from flask import Flask, redirect, render_template, current_app
#running behind proxy?                                                                                            
from werkzeug.middleware.proxy_fix import ProxyFix

#Blueprints
from api.api import api_bp
from config import myconfig
from game_initale.game_initiale import initiale_bp
from game_melimelo.game_melimelo import melimelo_bp
from game_pendu.game_pendu import pendu_bp
from game_random.game_random import random_bp
from game_listening.game_listening import listening_bp

# NOT using pokebase in the end, the performances are so badm it takes 3-5 sec to get the object though calling the URL + parsing the json is < 250ms
#import pokebase
#use my poor man reimplementation with cache
from poorman_pokeapi_client import Pokepoor

########################################################################################
## Flask vars
#
app = Flask(__name__, static_url_path='')
app.secret_key = myconfig["session secret key"]

#if behind a proxy set the WSGI properly 
# see http://electrogeek.tokyo/setup%20flask%20behind%20nginx%20proxy.html
if myconfig.get("BehindProxy", False):
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
@app.route('/home')
def homepage():
    gamecards = []
    for bp in app.blueprints.values():
        if hasattr(bp, "htmlRenderHomepageCard"):
            gamecards.append(bp.htmlRenderHomepageCard())


    return render_template("home01.html", pagename="Home", gamecards=gamecards, logo= Pokepoor.getPokemon(random.randrange(1, myconfig["max pokemon id"])).spriteURL, **current_app.global_render_template_params)


@app.before_request
def set_global_variables():
    headerz = []
    for bp in app.blueprints.values():
        if hasattr(bp, "htmlRenderPageHeader"):
            headerz.append(bp.htmlRenderPageHeader())
    current_app.global_render_template_params = {"headerz": headerz} 

#-----------------------------------------------------------------------
#Get a random pokemon, good for debugging
app.register_blueprint(random_bp)
    
#-----------------------------------------------------------------------
#GAME A : find the initiale/first letter of a Pokemon!
app.register_blueprint(initiale_bp)
    
#-----------------------------------------------------------------------
#GAME B : pendu type of game
app.register_blueprint(pendu_bp)
    
#-----------------------------------------------------------------------
#GAME C : "meli-melo" put the letters of the pokemon in the right order
#app.register_blueprint(melimelo_bp)

#-----------------------------------------------------------------------
#REST API to change the language
app.register_blueprint(api_bp, url_prefix='/api')

#-----------------------------------------------------------------------
#GAME LISTENING : write a word you heard
app.register_blueprint(listening_bp)


########################################################################################
## Main entry point
#
if __name__ == '__main__':
    try:
        #logging
        directory = os.path.dirname(myconfig.get("logfile", "/tmp/poketrainer.log"))
        if not os.path.exists(directory):
            os.makedirs(directory)

        logging.basicConfig(filename=myconfig.get("logfile", "/tmp/poketrainer.log"), level=logging.WARN)

        app.logger.warning("Starting the app")

        #run the subdirectory if needed
        if "subdirectory" in myconfig:
            myconfig["subdirectory"](app)

        #start web interface
        app.debug = True
        app.run(host='0.0.0.0', port=myconfig.get("port", 12345), threaded=True)

    except Exception as e:
        print("Error in main: %s" % str(e))
        app.logger.error("Error in main: %s" % str(e))
        raise