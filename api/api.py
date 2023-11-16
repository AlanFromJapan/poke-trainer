from flask import Blueprint
import requests
from config import myconfig

api_bp = Blueprint('api_bp', __name__)

@api_bp.route("/language/<lang>", methods=['PUT'])
def setLanguage(lang):
    print(f"Language change callback: {myconfig['language']} => {lang}.")
    myconfig['language'] = lang
    return "OK"


@api_bp.route("/letterstyle/<style>", methods=['PUT'])
def setLetterStyle(style):
    print(f"Letter style changed to: {myconfig['letterstyle']} => {style}.")
    myconfig['letterstyle'] = style
    return "OK"


@api_bp.route("/lettercase/<case>", methods=['PUT'])
def setLetterCase(case):
    print(f"Letter case changed to: {myconfig['lettercase']} => {case}.")
    myconfig['lettercase'] = case
    return "OK"


#Indirection so I can keep the API key on server side (useless, but I don't want to expose it)
@api_bp.route("/speech2text/<lang>/<message>", methods=['GET'])
def speech2Text(lang, message):
    print(f"S2T: {lang} - '{message}'")
    req = requests.Request('GET', f"https://api.voicerss.org/?key={myconfig['VoiceRSS key']}&hl={lang}&c=MP3&v=Zola&f=16khz_16bit_mono&src={message}")
    prepared = req.prepare()
    resp = requests.Session().send(prepared, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()