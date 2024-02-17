from games.frc_game import FRCGame
from analysis.stat import Stat, LinkedStat, SumStat, CustomStat, PostStat
from analysis.simulator import get_random_schedule, simulate_event, get_clean_schedule, get_qual_matches
from analysis.chart import Chart, ChartField
import numpy as np

class Crescendo2024(FRCGame):
    def __init__(self):

        self.preprocessors = [
        ]

        self.stats = [
            CustomStat('Rank', self.assign_ranks, report_stat=True, order = 1),

            # Declare all Source Stats
            Stat('autoAmpNoteCount'),
            Stat('autoSpeakerNoteCount'),
            # Stat('endGameNoteInTrapPoints'),
            Stat('teleopAmpNoteCount'),
            Stat('teleopSpeakerNoteAmplifiedCount'),
            Stat('teleopSpeakerNoteCount'),


            # Create Linked Stats
            LinkedStat('autoLinePoints','autoLineRobot', {"Yes":2,"No":0}),
            LinkedStat('climb','endGameRobot',{"Parked":1, "StageLeft":3, "StageRight": 3, "CenterStage":3, "None":1}),


            # Calculate Who scored which traps
            CustomStat('trapNoteCount', self.calc_trap_notes),
            # Aggregate Stats Based upon Placement Position and Type
            SumStat('autoPoints',[
                'autoAmpNoteCount',
                'autoLinePoints',
                'autoSpeakerNoteCount',
            ], weights = [2,1,5], order=3),

            SumStat('teleopPoints',[
                'teleopSpeakerNoteAmplifiedCount',
                'teleopSpeakerNoteCount',
                'teleopAmpNoteCount',
            ], weights = [
                5,2,1
            ],
            display_name="Teleop", report_stat = True, order=4),

            SumStat('endgamePoints',[
                'climb',
                'trapNoteCount',
            ], 
            weights = [1,5],
            display_name="End Game", report_stat = True, order=5),


            SumStat('noteCount',[
                'trapNoteCount',
                'autoAmpNoteCount',
                'autoSpeakerNoteCount',
                'teleopAmpNoteCount',
                'teleopSpeakerNoteCount',
                'teleopSpeakerNoteAmplifiedCount'
            ], report_stat = True, display_name = 'Notes', order=2),


            SumStat('OPR',[
                'teleopPoints',
                'autoPoints',
                'endgamePoints'
            ], display_name="OPR", report_stat = True, order=0),

            # 
            # SumStat('simulatedRanking',[]),
            # SumStat('expectedRanking',[], display_name='Expected Ranking', report_stat = True),
            # PostStat('schedule', self.calc_schedule, display_name='Schedule', report_stat = True)
        ]

        self.charts = [
            Chart('OPR', [
                ChartField('teleopPoints', display_text='Teleop'),
                ChartField('autoPoints', display_text='Auto'),
                ChartField('endgamePoints', display_text='EndGame')
            ])
        ]

  
    # Performs best guess calculations on who is scoring each trap each match
    def calc_trap_notes(self, played_matches:list, teams:list, stat:dict, rankings:dict) -> dict:
        for team in teams:
            stats = teams[team]
            stats['trapNoteCount'] = 0
        return teams
        

    # Assigns Event Rankings to all the Teams at the event
    def assign_ranks(self, played_matches:list, teams:list, stat:dict, rankings:dict)-> dict:
        if(rankings != None):
            for rank in rankings['rankings']:
                teams[rank['team_key']]['rank'] = rank['rank']
        else:
            for team in teams:
                teams[team]['rank'] = 0
        return teams

    def calc_schedule(self, matches:list, teams:list, stat:dict, rankings:dict)-> dict:
        # team_rps = {}
        # for team in teams:
        #     team_rps[team] = {'rp':0}


        # for match in matches:
        #     for color in ['red','blue']:
        print("Matches" ,len(matches))
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

        num_sims = 1000
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
            # print(sum(rps[rank[0]]) / num_sims, expected_rp[rank[0]])
            schedule_adjust += expected_rp[rank[0]] / (sum(rps[rank[0]]) / num_sims)
            count +=1

        
        schedule_adjust = schedule_adjust / (len(ranks))

        print(schedule_adjust)
        count = 1
        avg_percentile = 0

        for rank in rankings:
            teams[rank[0]]['expectedRanking'] = count
            # teams[rank[0]]['schedule'] = teams[rank[0]]['simulatedRanking'] - count
            rp_distribution = sorted(rps[rank[0]])
            # lb = np.searchsorted(rp_distribution, expected_rp)
            percentile = (np.searchsorted(rp_distribution, expected_rp[rank[0]], side="left")) / num_sims * 100

            # print(rank[0], percentile)
            teams[rank[0]]['schedule'] = percentile
            avg_percentile += percentile
            print(count, rank[0][3:], qual_rp[rank[0]], percentile, teams[rank[0]])
            count +=1
            
        print("Average Percentile", avg_percentile / (len(rankings)))
        return teams

    def validate_match(self, match:dict) -> bool:
        return True

    def predict_alliance(self, color:str, match:dict, teams:dict, prediction:dict):

        endgame = 0
        auto_charge_station = 0

        auto_elements = 0

        high_cubes = 0
        mid_cubes = 0

        high_cones = 0
        mid_cones = 0

        low = 0
        supercharged = 0
        for team_key in match.get('alliances',{}).get(color,{}).get('team_keys',[]):
            team = teams.get(team_key,{})
            auto_elements += team.get('autoHighCubes',0) + team.get('autoHighCones',0) + team.get('autoMidCubes',0) + team.get('autoMidCones',0) + team.get('autoLow',0)
            high_cubes += team.get('autoHighCubes',0) + team.get('teleopHighCubes',0)
            high_cones += team.get('autoHighCones',0) + team.get('teleopHighCones',0)

            mid_cubes += team.get('autoMidCubes',0) + team.get('teleopMidCubes',0)
            mid_cones += team.get('autoMidCones',0) + team.get('teleopMidCones',0)

            low += team.get('autoLow',0) + team.get('teleopLow',0)
            
            # endgame += team.get('endgamePoints',0)
            auto_charge_station = max(auto_charge_station, team.get('autoChargeStation',0))

        high_cubes = round(high_cubes)
        high_cones = round(high_cones)
        mid_cubes = round(mid_cubes)
        mid_cones = round(mid_cones)
        low = round(low)

        if match.get('comp_level') == 'qm':
            endgame = 22
        else:
            endgame = 30


        if high_cubes > 3:
            mid_cubes += high_cubes -3
            high_cubes = 3
        
        if high_cones > 6:
            mid_cones += high_cones - 6
            high_cones = 6
        
        if mid_cubes > 3:
            low += mid_cubes - 3
            mid_cubes = 3
        
        if mid_cones > 6:
            low += mid_cones - 6
            mid_cones = 3

        if low > 9:
            if high_cubes >=3 and high_cones >=3 and mid_cubes >=3 and mid_cones >=3:
                supercharged = low - 9
            low = 9

        high_links = int(min(high_cubes, high_cones / 2.0))
        mid_links = int(min(mid_cubes, mid_cones / 2.0))
        low_links = int(low / 3.0)

        links = high_links + mid_links + low_links

        score = links * 5 + (high_cubes + high_cones) * 5 + (mid_cubes + mid_cones) * 3 + low * 2 + auto_elements + auto_charge_station + endgame + 3 * supercharged

        prediction[f"{color}_teams"] = match.get('alliances',{}).get(color,{}).get('team_keys',[])
        prediction[f"{color}_score"] = round(score,2)
        prediction[f"{color}_highCubes"] = round(high_cubes,2)
        prediction[f"{color}_highCones"] = round(high_cones,2)
        prediction[f"{color}_midCubes"] = round(mid_cubes,2)
        prediction[f"{color}_midCones"] = round(mid_cones,2)
        prediction[f"{color}_low"] = round(low)
        prediction[f"{color}_links"] = round(links)
        prediction[f"{color}_autoChargeStation"] = round(auto_charge_station,2)
        prediction[f"{color}_endGame"] = round(endgame,2)
        prediction[f"{color}_autoElements"] = round(auto_elements,2)
        prediction[f"{color}_chargeStation"] = round(auto_charge_station) + round(endgame)

        result_time = match.get('post_result_time',-1)
        if result_time != None and result_time > 0 :
            prediction[f"{color}_actual_score"] = match.get('alliances',{}).get(color,{}).get('score',-1)




    def predict_match(self, match:dict, teams:dict) -> dict:


        prediction = {
            'comp_level': match.get('comp_level', 'unknown'),
            'key': match.get('key', 'unknown'),
            'match_number': match.get('match_number',0),
            'set_number': match.get('set_number',0)
        }
        

        self.predict_alliance('blue', match, teams, prediction)
        self.predict_alliance('red', match, teams, prediction)
        

        

        if prediction['blue_score'] > prediction['red_score']:
            prediction['blue_win_rp'] = 2
            prediction['red_win_rp'] = 0
        elif prediction['blue_score'] < prediction['red_score']:
            prediction['blue_win_rp'] = 0
            prediction['red_win_rp'] = 2
        else:
            prediction['blue_win_rp'] = 1
            prediction['red_win_rp'] = 1

        if prediction['blue_chargeStation'] > 26:
            prediction['blue_charge_rp'] = 1
        else:
            prediction['blue_charge_rp'] = 0
        
        if prediction['red_chargeStation'] > 26:
            prediction['red_charge_rp'] = 1
        else:
            prediction['red_charge_rp'] = 0

        if prediction['blue_links'] >= 6:
            prediction['blue_link_rp'] = 1
        elif prediction['red_links'] >= 2 and prediction['blue_links'] >= 5:
            prediction['blue_link_rp'] = 1
        else:
            prediction['blue_link_rp'] = 0

        if prediction['red_links'] >= 6:
            prediction['red_link_rp'] = 1
        elif prediction['blue_links'] >=2 and prediction['red_links'] >= 5:
            prediction['red_link_rp'] = 1
        else:
            prediction['red_link_rp'] = 0

        return prediction
    
    def parse_rps(self, match:dict) -> tuple:
        blue_rp = 0
        red_rp = 0
        
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('activationBonusAchieved'))
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('sustainabilityBonusAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('activationBonusAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('sustainabilityBonusAchieved'))
        # coop_red = match.get('score_breakdown',{}).get('red',{}).get('coopertitionCriteriaMet')
        # coop_blue = match.get('score_breakdown',{}).get('blue',{}).get('coopertitionCriteriaMet')

        # coop = coop_red and coop_blue


        # blue_links = len(match.get('score_breakdown',{}).get('blue',{}).get('links',[]))
        # red_links = len(match.get('score_breakdown',{}).get('red',{}).get('links',[]))


        # if blue_links >=6 or (blue_links >=5 and coop):
        #     blue_rp +=1
        
        # if red_links >=6 or (red_links >=5 and coop):
        #     red_rp +=1




        blue_score = match.get('score_breakdown',{}).get('blue',{}).get('totalPoints',0)
        red_score = match.get('score_breakdown',{}).get('red',{}).get('totalPoints',0)

        if blue_score > red_score:
            blue_rp +=2
        elif red_score > blue_score:
            red_rp +=2
        else:
            blue_rp +=1 
            red_rp +=1

        return (blue_rp,red_rp)

    def validate_match(self, match:dict) -> bool:
        passing = True
        passing = 'frc0' not in match.get('alliances',{}).get('blue',{}).get('team_keys',[]) and passing
        passing = 'frc0' not in match.get('alliances',{}).get('red',{}).get('team_keys',[]) and passing
        return passing
