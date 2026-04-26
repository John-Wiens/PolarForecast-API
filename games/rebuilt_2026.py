from games.frc_game import FRCGame
from analysis.stat import Stat, LinkedStat, SumStat, CustomStat, PostStat
from analysis.chart import Chart, ChartField
from analysis.simulator import get_random_schedule, simulate_event, get_clean_schedule, get_qual_matches
import numpy as np

class Rebuilt2026(FRCGame):
    def __init__(self):
        self.preprocessors = [
            self.flatten_hub
        ]

        self.stats = [
            CustomStat('rank', self.assign_ranks, report_stat=True),
            Stat('autoCount'),
            Stat('teleopCount'),

            Stat('transitionCount'),
            Stat('shift1Count'),
            Stat('shift2Count'),
            Stat('shift3Count'),
            Stat('shift4Count'),
            Stat('endgameCount'),

            SumStat('scoringWindow1Count',[
                'shift1Count',
                'shift2Count',
            ]),

            SumStat('scoringWindow2Count',[
                'shift3Count',
                'shift4Count',
            ]),

            LinkedStat('autoTower','autoTowerRobot', {"None":0, "Level1":15}),
            LinkedStat('endGameTower','endGameTowerRobot', {"None":0, "Level1":10, "Level2":20, "Level3":30}),
            
            SumStat('auto',[
                'autoTower', 
                'autoCount'
            ], report_stat = True, order=2),

            SumStat('tower',[
                'autoTower', 
                'endGameTower'
            ], report_stat = True, order=3),

            SumStat('teleop', [
                'teleopCount',
            ], report_stat = False, order=3),

            SumStat('fuel', [
                'autoCount',
                'teleopCount',
            ], report_stat = True, order =1),
          

            SumStat('OPR', [
                'fuel',
                'autoTower',
                'endGameTower'
            ],report_stat = True, order = 0),

            SumStat('simulatedRanking',[]),
            SumStat('expectedRanking',[], display_name='Expected Ranking', report_stat = True, order = 4),
            PostStat('schedule', self.calc_schedule, display_name='Schedule', report_stat = True, order = 5)
  
        ]

        self.charts = [
            Chart('OPR', [
                ChartField('teleop', display_text='Teleop'),
                ChartField('auto', display_text='Auto'),
                ChartField('endGameTower', display_text='EndGame')],
            ),
            Chart('Total Fuel Scored', [
                ChartField('autoCount', display_text='auto'),
                ChartField('teleopCount', display_text='teleop')
                ],
            ),
            Chart('Tower', [
                ChartField('autoTower', display_text='Auto Tower'),
                ChartField('endGameTower', display_text='Endgame Tower'),
                ],
            ),
            Chart('Elements per Scoring Period', [
                ChartField('autoCount', display_text='Auto'),
                ChartField('teleopCount', display_text='Teleop')],
            ),
            Chart('Elements per Scoring Window',[
                ChartField('autoCount', display_text='Auto'),
                ChartField('transitionCount', display_text='Transition'),
                ChartField('scoringWindow1Count', display_text='Window 1'),
                ChartField('scoringWindow2Count', display_text='Window 2'),
                ChartField('endgameCount', display_text='End Game'),
            ])
        ]

    def flatten_hub(self, played_matches:list, teams:dict):
        for match in played_matches:
            for color in ['blue','red']:
                for key in match.get('score_breakdown',{}).get(color,{}).get('hubScore',{}).keys():
                    match['score_breakdown'][color][key] = match.get('score_breakdown',{}).get(color,{}).get('hubScore',{}).get(key,0)

        return played_matches, teams

    # Assigns Event Rankings to all the Teams at the event
    def assign_ranks(self, played_matches:list, teams:list, stat:dict, rankings:dict)-> dict:
        if rankings is not None:
            for rank in rankings.get('rankings', []):
                teams[rank['team_key']]['rank'] = rank['rank']
        return teams

    def validate_match(self, match:dict) -> bool:
        return True
    
    def calc_schedule(self, matches:list, teams:list, stat:dict, rankings:dict)-> dict:
        clean_matches = get_clean_schedule(matches)
        qual_matches = get_qual_matches(matches)
        if len(clean_matches) == 0:
            opr_teams = sorted(teams.items(), key=lambda x:x[1]['OPR'], reverse = True)
            count = 1
            for team in opr_teams:
                teams[team[0]]['expectedRanking'] = count
                teams[team[0]]['simulatedRanking'] = count
                teams[team[0]]['schedule'] = 0
                teams[team[0]]['rank'] = 0
                count += 1
            return teams

        rps = {}
        ranks = {}
        for team in teams:
            ranks[team] = []
            rps[team] = []

        num_sims = 100
        for i in range(0,num_sims):
            simulated_schedules = get_random_schedule(teams, len(clean_matches))
            simulated_rps = simulate_event(simulated_schedules, teams, self.predict_match, self.parse_rps)
            rankings = sorted(simulated_rps.items(), key=lambda x:x[1], reverse = True)
            rank = 1

            for team in rankings:
                ranks[team[0]].append(rank)
                rps[team[0]].append(simulated_rps[team[0]])
                rank +=1


        expected_rp = simulate_event(clean_matches, teams, self.predict_match, self.parse_rps)
        qual_rp = simulate_event(qual_matches, teams, self.predict_match, self.parse_rps)
        rankings = sorted(qual_rp.items(), key=lambda x:x[1], reverse = True)

        ranks = sorted(ranks.items(), key=lambda x:sum(x[1]))
        count = 1
        schedule_adjust = 0

        for rank in ranks:
            teams[rank[0]]['simulatedRanking'] = count
            schedule_adjust += expected_rp[rank[0]] / (sum(rps[rank[0]]) / num_sims)
            count +=1

        
        schedule_adjust = schedule_adjust / (len(ranks))

        count = 1
        avg_percentile = 0

        for rank in rankings:
            teams[rank[0]]['expectedRanking'] = count
            rp_distribution = sorted(rps[rank[0]])
            percentile = (np.searchsorted(rp_distribution, expected_rp[rank[0]], side="left")) / num_sims * 100

            teams[rank[0]]['schedule'] = percentile
            avg_percentile += percentile
            count +=1
            
        return teams
    
    
    def parse_rps(self, match:dict) -> tuple:
        blue_rp = 0
        red_rp = 0
        
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('energizedAchieved'))
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('superchargedAchieved'))
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('traversalAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('energizedAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('superchargedAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('traversalAchieved'))


        blue_score = match.get('score_breakdown',{}).get('blue',{}).get('totalPoints',0)
        red_score = match.get('score_breakdown',{}).get('red',{}).get('totalPoints',0)

        if blue_score > red_score:
            blue_rp +=3
        elif red_score > blue_score:
            red_rp +=3
        else:
            blue_rp +=1 
            red_rp +=1

        return (blue_rp,red_rp)

    def predict_alliance(self, color:str, match:dict, teams:dict, prediction:dict):
        final_score = 0
        total_fuel = 0
        total_tower = 0
        for team_key in match.get('alliances',{}).get(color,{}).get('team_keys',[]):
            fuel = teams.get(team_key,{}).get('fuel',0)
            tower = teams.get(team_key,{}).get('tower',0)
            final_score += fuel + tower
            

        prediction[f"{color}_score"] = final_score
        prediction[f"{color}_fuel"] = total_fuel
        prediction[f"{color}_tower"] = total_tower


        if total_fuel >= 360:
            prediction[f"{color}_energized_rp"] = 1
        else:
            prediction[f"{color}_energized_rp"] = 0

        if total_fuel >= 100:
            prediction[f"{color}_supercharged_rp"] = 1
        else:
            prediction[f"{color}_supercharged_rp"] = 0

        if total_tower >= 55:
            prediction[f"{color}_traversal_rp"] = 1
        else:
            prediction[f"{color}_traversal_rp"] = 0

    def predict_match(self, match:dict, teams:dict) -> dict:
        prediction = {
            'comp_level': match.get('comp_level', 'unknown'),
            'key': match.get('key', 'unknown'),
            'match_number': match.get('match_number',0),
            'set_number': match.get('set_number',0)
        }

        self.predict_alliance('blue', match, teams, prediction)
        self.predict_alliance('red', match, teams, prediction)

        # Assign RP for Winning the Match
        if prediction['blue_score'] > prediction['red_score']:
            prediction['blue_win_rp'] = 3
            prediction['red_win_rp'] = 0
        elif prediction['blue_score'] < prediction['red_score']:
            prediction['blue_win_rp'] = 0
            prediction['red_win_rp'] = 3
        else:
            prediction['blue_win_rp'] = 1
            prediction['red_win_rp'] = 1

        return prediction
