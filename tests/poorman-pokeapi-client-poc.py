import requests
import json

URL="https://pokeapi.co/api/v2/pokemon/<ID>/"

resp = requests.get(URL.replace("<ID>", str(1)))

j = json.loads(resp.text)

desc= f"""
Name :  {j["name"]}
ID:     {j["id"]}
species:{j["species"]["name"]}
sprites:<img src="{j["sprites"]["front_default"]}" />    
"""
print(desc)