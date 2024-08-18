# poke-trainer
App to help kids to learn to read with Pokemons (based on **pokeapi** https://pokeapi.co/)

Could be multilingual, most likely won't for it's already a miracle if I have time to write it to a useable state somehow. Will try to not make it completely language-locked if I can.

## What
Basically having young kids at home, poke-addicted, so it's a good way to use that to teach them a bit of reading, pronounciation, etc while having fun learning pokemon names while it lasts.

## Technicalities
I was planning to use the lib *pokebase* but it's SO SLOW it's unuseable. Apparently it's an issue that was raised 5 years ago and never fixed. I guess we all implemented a poor man request() -> get the json -> parse the 3 values you need and it's still only 10 lines of code but 10 times faster. Shame.

# Execute

## Run standalone
1. Make a virtual env `python -m venv .`
1. `source bin/activate`
1. `python -m pip install -r requirements.txt`
1. `python poke-trainer.py`

## Run in a Docker container
1. `docker build -t "poke"`
1. `docker run "poke"`
