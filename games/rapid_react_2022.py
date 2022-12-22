from games.frc_game import FRCGame
from analysis.stat import Stat, LinkedStat, SumStat, CustomStat



class RapidReact2022(FRCGame):
    def __init__(self):
        self.stats = [
            Stat('autoCargoLowerBlue'),
            LinkedStat('autoTaxi','taxiRobot', {"Yes":2,"No":0}),
            SumStat('auto', ['autoCargoLowerBlue', 'autoTaxi'], report_stat=True),
            CustomStat('rank', self.assign_ranks, report_stat=True)
        ]

        self.rp_functions = [
            self.get_climb_rp,
            self.get_ball_rp,
        ]

    # Assigns Event Rankings to all the Teams at the event
    def assign_ranks(self, played_matches:list, teams:list, stat:dict, rankings:dict)-> dict:
        for rank in rankings['rankings']:
            teams[rank['team_key']]['rank'] = rank['rank']
        return teams

    def validate_match(self, match:dict) -> bool:
        return True

    def predict_match(self, match:dict, teams:dict) -> dict:
        print("Predicting Match", match)
        # prediction = []
        # if(match.get('post_result_time',0) != 0):
        #     predict_alliance('blue', match, teams)
            
        # else:
        #     pass
        return {}

    def predict_alliance(self, color:str, match:dict, teams:dict):
        # for team_key in match.get('alliances',{}).get('blue',{}).get(team_keys,[]):
        #         prediction[f"{color}_score"] = teams.get(teak_key,{}).get()
        pass       


    def get_climb_rp(self, match:dict) -> tuple:
        return (0,0)

    def get_ball_rp(self, match) -> tuple:
        return (0,0)
