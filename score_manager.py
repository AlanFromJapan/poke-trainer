from flask import session, current_app

#This is an abstract class for score manager, compiles but would not run
class score_manager():
    def __init__(self):
        #nothing to do here
        pass


    def score_storage(self):
        # This is an abstract method, it should be implemented in the derived class
        return None


    def set_score(self, game, score):
        store = self.score_storage()
        store[game] = score


    def get_score(self, game):
        store = self.score_storage()
        return store[game] if game in store else 0


    def reset_score(self, game):
        self.set_score(game, 0)


    def inc_score(self, game):
        self.set_score(game, self.get_score(game) +1)
        #not calling session modifier because it is done in set_score



# This is a session based score manager
class score_manager_session(score_manager):
    def __init__(self):
        super().__init__()

    #stores the score in the session
    def score_storage(self):
        if "score_session" not in session:
            session["score_session"] = {}

        return session["score_session"]


    def set_score(self, game, score):
        super().set_score(game, score)
        # This change is not picked up because a mutable object is not detected as changed (changing the CONTENT of the dictionary)
        # so mark it as modified yourself (RTFM https://flask.palletsprojects.com/en/2.3.x/api/#flask.session)
        session.modified = True


    def reset_score(self, game):
        super().reset_score(game)
        # This change is not picked up because a mutable object is not detected as changed (changing the CONTENT of the dictionary)
        # so mark it as modified yourself (RTFM https://flask.palletsprojects.com/en/2.3.x/api/#flask.session)
        session.modified = True

