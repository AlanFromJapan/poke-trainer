myconfig = {
    "max pokemon id": 150,
    "language" : "fr",

    "gameA cards" : 5,

    "session secret key" : "you can really put whatever you want, it's just to encrypt the thingy!",

    #Normally this should be True, but in case you use this where someone misconfigured the CA check settings then make this False.
    "SSL_CHECK" : True,

    #if true, will print some stats about the cache etc.
    "Show stats" : False,

    "BehindProxy" : False,

    #Block, Cursive or mix
    "letterstyle" : "block",

    #uppercase or lowercase
    "lettercase" : "lowercase",

    #VoiceRSS key for speech to text
    "VoiceRSS key" : "your key here",

    #where is the logfile
    "logfile" : "/tmp/poke-trainer.log",

    #TCP port number to listen to
    "port" : 56788,
}