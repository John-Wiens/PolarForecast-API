from games.frc_game import FRCGame
from analysis.stat import Stat, LinkedStat, SumStat, CustomStat



class RapidReact2022(FRCGame):
    def __init__(self):
        self.stats = [
            CustomStat('rank', self.assign_ranks, report_stat=True),
            Stat('autoCargoLowerBlue'),
            Stat('autoCargoLowerRed'),
            Stat('autoCargoLowerFar'),
            Stat('autoCargoLowerNear'),
            Stat('autoCargoUpperBlue'),
            Stat('autoCargoUpperRed'),
            Stat('autoCargoUpperFar'),
            Stat('autoCargoUpperNear'),

            Stat('teleopCargoLowerBlue'),
            Stat('teleopCargoLowerRed'),
            Stat('teleopCargoLowerFar'),
            Stat('teleopCargoLowerNear'),
            Stat('teleopCargoUpperBlue'),
            Stat('teleopCargoUpperRed'),
            Stat('teleopCargoUpperFar'),
            Stat('teleopCargoUpperNear'),
            
            LinkedStat('autoTaxi','taxiRobot', {"Yes":2,"No":0}),
            

            SumStat('autoCargoHigh',[
                'autoCargoUpperRed', 
                'autoCargoUpperBlue', 
                'autoCargoUpperFar', 
                'autoCargoUpperNear'
            ]),

            SumStat('autoCargoLow', [
                'autoTaxi',
                'autoCargoLowerBlue', 
                'autoCargoLowerRed',
                'autoCargoLowerFar',
                'autoCargoLowerNear' 
            ]),

            SumStat('auto',[
                'autoTaxi',
                'autoCargoHigh',
                'autoCargoLow',
            ], weights = [
                1,4,2
            ], report_stat = True),

            SumStat('teleopCargoHigh',[
                'teleopCargoUpperRed', 
                'teleopCargoUpperBlue', 
                'teleopCargoUpperFar', 
                'teleopCargoUpperNear'
            ]),

            SumStat('teleopCargoLow', [
                'teleopCargoLowerBlue', 
                'teleopCargoLowerRed',
                'teleopCargoLowerFar',
                'teleopCargoLowerNear' 
            ]),

            SumStat('cargo', [
                'autoCargoLow',
                'autoCargoHigh', 
                'teleopCargoLow',
                'teleopCargoHigh'
            ]),

            SumStat('teleop', [
                'teleopCargoHigh',
                'teleopCargoLow',
            ], weights = [
                2,1
            ], report_stat = True),

            LinkedStat('endgame','endgameRobot', {"Traversal":15,"High":10, "Mid":6, "Low":4, "None":0}, report_stat=True),

            SumStat('OPR', [
                'auto',
                'teleop',
                'endgame'
            ],report_stat = True),
  
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

    def predict_alliance(self, color:str, match:dict, teams:dict, prediction:dict):
        score = 0
        cargo = 0
        endgame = 0
        for team_key in match.get('alliances',{}).get(color,{}).get('team_keys',[]):
            score = teams.get(team_key,{}).get('OPR',0)
            cargo = teams.get(team_key,{}).get('cargo',0)
            endgame = teams.get(team_key,{}).get('endgame',0)

        prediction[f"{color}_score"] = score
        prediction[f"{color}_cargo"] = cargo
        prediction[f"{color}_endgame"] = endgame


        if cargo >= 20:
            prediction[f"{color}_rp_1"] = 1
        else:
            prediction[f"{color}_cargo_rp"] = 0

        if endgame >= 20:
            prediction[f"{color}_climb_rp"] = 1
        else:
            prediction[f"{color}_climb_rp"] = 0

    def predict_match(self, match:dict, teams:dict) -> dict:
        print(match)
        #print("Predicting Match", match)
        prediction = {
            'comp_level': match.get('comp_level', 'unknown'),
            'key': match.get('key', 'unknown'),
            'match_number': match.get('match_number',0),
        }

        self.predict_alliance('blue', match, teams, prediction)
        self.predict_alliance('red', match, teams, prediction)

        return prediction

         


    def get_climb_rp(self, match:dict) -> tuple:
        return (0,0)

    def get_ball_rp(self, match:dict) -> tuple:
        return (0,0)
