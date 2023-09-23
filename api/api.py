from flask import Blueprint

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