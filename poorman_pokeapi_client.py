import requests
import json
#for the caching decorator
from functools import lru_cache
import datetime

URL_MAIN="https://pokeapi.co/api/v2/pokemon/<ID>/"
URL_SPECIES="https://pokeapi.co/api/v2/pokemon-species/<ID>"


class Pokepoor:
    name = ""
    id = 0
    species = []
    spriteURL = ""
    spriteURL_big = ""
    #maps language to translation (ie: "fr" -> "Bulbizarre")
    translations= {}

    def __init__(self, name, id, species, sprite) -> None:
        self.name = name
        self.id = id
        self.species = species
        self.spriteURL = sprite
        self.spriteURL_big = ""

    
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


    #there's 150 legacy pokemon so should cover them all... LRU part is not used though (shrug)
    @lru_cache(maxsize=180)
    #Returns a pokemon details
    def getPokemon(id:int) -> "Pokepoor":
        #######
        ## 1- get basics
        #
        resp = requests.get(URL_MAIN.replace("<ID>", str(id)))

        j = json.loads(resp.text)

        p = Pokepoor(j["name"], j["id"], j["species"]["name"], j["sprites"]["front_default"])

        #try to get a BIG image if exists
        try:
            p.spriteURL_big = j["sprites"]["other"]["official-artwork"]["front_default"]
        finally:
            pass

        #######
        ## 2- get name translations
        #
        resp = requests.get(URL_SPECIES.replace("<ID>", str(id)))

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

    print(p)
