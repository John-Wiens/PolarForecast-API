

#
# FRC Game is a generic class to be used as a parent for game specific classes. 
# It contains stubbed out methods that child classes should implement to ensure a consistent model can be used across multiple seasons to reduce boilerplate.
#

class FRCGame():

    rp_functions = []
    stats = []
    game_name = "Generic FRC Game"

    def __init__(self):
        pass

    # Returns true if the match is , should be overridden by each years individual game
    def validate_match(self, match:dict) -> bool:
        print("Match Validation has not been implemented for this game. All Matches are assumed to be valid.")
        return True


    def predict_match(self, match:dict) -> dict:
        print("Match Prediction has not been implemented for this game.")
        return {}
    

    




