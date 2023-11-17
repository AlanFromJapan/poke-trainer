
# The languageItem class that contains basic data about a word to find
class LanguageItem:
    toType : str = None
    toHear : str = None
    #URL to the image
    toSee : str = None 
    #the language of the word to find (fr, jp, ko, etc.)
    lang2 : str = None
    #the language of the word to find (fr-fr, ja-jp, ko-kr, etc.)
    lang4 : str = None

    def __init__(self, toType, toHear, toSee, lang2):
        self.toType = toType
        self.toHear = toHear
        self.toSee = toSee
        self.lang2 = lang2
        self.lang4 = self.language2chars_4chars()

    def language2chars_4chars(self):
        #this will deserve be improved if we want to support more languages
        return "fr-fr" if self.lang2 == "fr" else "ja-jp" if self.lang2 == "jp" else "ko-kr"
    

    def __str__(self):
        return f"toType: {self.toType}\ntoHear: {self.toHear}\ntoSee: {self.toSee}\nlang2: {self.lang2}"