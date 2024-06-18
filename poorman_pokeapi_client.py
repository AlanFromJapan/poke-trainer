import requests
import json
#for the caching decorator
from functools import lru_cache
import datetime
import config
from flask import current_app as app


URL_MAIN="https://pokeapi.co/api/v2/pokemon/<ID>/"
URL_SPECIES="https://pokeapi.co/api/v2/pokemon-species/<ID>"


class Pokepoor:
    def __init__(self, name, id, species, sprite) -> None:
        self.name = name
        self.id = id
        self.species = species
        self.spriteURL = sprite
        self.spriteURL_big = ""
        #maps language to translation (ie: "fr" -> "Bulbizarre")
        self.translations= {}    

    
    def __str__(self) -> str:
        desc= f"""
Name :          {self.name}
ID:             {self.id}
species:        {self.species}
sprites:        {self.spriteURL}
sprites (big):  {self.spriteURL_big}
Translations:
"""
        for k in self.translations.keys():
            desc = desc + f"                  - {k}: {self.translations[k]}\n" 

        return desc

    def __hash__(self) -> int:
        return int(self.id)
    
    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id
    

    #there's 150 legacy pokemon so should cover them all... LRU part is not used though (shrug)
    @lru_cache(maxsize=180)
    #Returns a pokemon details
    def getPokemon(id:int) -> "Pokepoor":
        #######
        ## 0- cache fault
        #
        app.logger.warning(f"Cache miss for {id}")
        print(__name__)

        #######
        ## 1- get basics
        #
        resp = requests.get(URL_MAIN.replace("<ID>", str(id)), verify=config.myconfig["SSL_CHECK"])

        j = json.loads(resp.text)

        p = Pokepoor(j["name"], j["id"], j["species"]["name"], j["sprites"]["front_default"])

        #try to get a BIG image if exists
        try:
            p.spriteURL_big = j["sprites"]["other"]["official-artwork"]["front_default"]
        except Exception as e:
            app.logger.warning("No big image for ", p.name)
            app.logger.warning(e)
            app.logger.warning("JSON was ", j)
            p.spriteURL_big = p.spriteURL

        #######
        ## 2- get name translations
        #
        resp = requests.get(URL_SPECIES.replace("<ID>", str(id)), verify=config.myconfig["SSL_CHECK"])

        j = json.loads(resp.text)
    
        for n in j["names"]:
            p.translations[n["language"]["name"]] = n["name"]

        return p


#Standalone test
if __name__ == '__main__':
    print("================= STANDALONE TEST")
    start = datetime.datetime.now()
    p = Pokepoor.getPokemon(1)
    end = datetime.datetime.now()
    print(f"Call 1: {end -start}")

    start = datetime.datetime.now()
    p = Pokepoor.getPokemon(2)
    end = datetime.datetime.now()
    print(f"Call 2: {end -start}")

    start = datetime.datetime.now()
    p = Pokepoor.getPokemon(2)
    end = datetime.datetime.now()
    print(f"Call 2 AGAIN: {end -start}")

    if config.myconfig["Show stats"]:
        #DBG check the cache
        print(Pokepoor.getPokemon.cache_info())
        
    print(p)
