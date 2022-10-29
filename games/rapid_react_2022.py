from games.frc_game import FRCGame
from analysis.stat import Stat, LinkedStat



class RapidReact2022(FRCGame):
    def __init__(self):
        self.stats = [
            Stat('autoCargoLowerBlue'),
            LinkedStat('autoTaxi','taxiRobot', {"Yes":2,"No":0})
        ]

        self.rp_functions = [
            self.get_climb_rp,
            self.get_ball_rp,
        ]

    def validate_match(self, match:dict) -> bool:
        return True

    def predict_match(self, match:dict) -> dict:
        return {}

    def get_climb_rp(self, match:dict) -> tuple:
        return (0,0)

    def get_ball_rp(self, match) -> tuple:
        return (0,0)
