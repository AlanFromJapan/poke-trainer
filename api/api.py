from flask import Blueprint, session, current_app
import requests
from config import myconfig

api_bp = Blueprint('api_bp', __name__)

@api_bp.route("/language/<lang>", methods=['PUT'])
def setLanguage(lang):
    print(f"Language change callback: {session['language']} => {lang}.")
    session['language'] = lang
    return "OK"


@api_bp.route("/letterstyle/<style>", methods=['PUT'])
def setLetterStyle(style):
    print(f"Letter style changed to: {session['letterstyle']} => {style}.")
    session['letterstyle'] = style
    return "OK"


@api_bp.route("/lettercase/<case>", methods=['PUT'])
def setLetterCase(case):
    print(f"Letter case changed to: {session['lettercase']} => {case}.")
    session['lettercase'] = case
    return "OK"


#Indirection so I can keep the API key on server side (useless, but I don't want to expose it)
@api_bp.route("/speech2text/<lang>/<message>", methods=['GET'])
def speech2Text(lang, message):
    print(f"S2T: {lang} - '{message}'")
    req = requests.Request('GET', f"https://api.voicerss.org/?key={myconfig['VoiceRSS key']}&hl={lang}&c=MP3&v=Zola&f=16khz_16bit_mono&src={message}")
    prepared = req.prepare()
    resp = requests.Session().send(prepared, stream=True, verify=myconfig["SSL_CHECK"])
    return resp.raw.read(), resp.status_code, resp.headers.items()


#Score manager
@api_bp.route("/score/<action>/<game>", methods=['GET'])
def score(action, game):
    current_app.logger.info(f"Score action {action} on game {game}")
    if action == "get":
        return current_app.global_render_template_params["scoremgr"].get_score(game)
    elif action == "inc":
        current_app.global_render_template_params["scoremgr"].inc_score(game)
    elif action == "reset":
        current_app.global_render_template_params["scoremgr"].reset_score(game)
    else:
        current_app.logger.error(f"Unknown action {action} for score on game {game}")
    
    return "OK"