from games.frc_game import FRCGame
from analysis.stat import Stat, LinkedStat, SumStat, CustomStat
from analysis.simulator import get_random_schedule, simulate_event


class ChargedUp2023(FRCGame):
    def __init__(self):

        self.preprocessors = [
            self.flatten_arrays
        ]

        self.stats = [
            CustomStat('rank', self.assign_ranks, report_stat=True),

            # Declare all Source Stats
            Stat('_autoCommunity_T_0'),
            Stat('_autoCommunity_T_1'),
            Stat('_autoCommunity_T_2'),
            Stat('_autoCommunity_T_3'),
            Stat('_autoCommunity_T_4'),
            Stat('_autoCommunity_T_5'),
            Stat('_autoCommunity_T_6'),
            Stat('_autoCommunity_T_7'),
            Stat('_autoCommunity_T_8'),
            
            Stat('_autoCommunity_M_0'),
            Stat('_autoCommunity_M_1'),
            Stat('_autoCommunity_M_2'),
            Stat('_autoCommunity_M_3'),
            Stat('_autoCommunity_M_4'),
            Stat('_autoCommunity_M_5'),
            Stat('_autoCommunity_M_6'),
            Stat('_autoCommunity_M_7'),
            Stat('_autoCommunity_M_8'),

            Stat('_autoCommunity_B_0'),
            Stat('_autoCommunity_B_1'),
            Stat('_autoCommunity_B_2'),
            Stat('_autoCommunity_B_3'),
            Stat('_autoCommunity_B_4'),
            Stat('_autoCommunity_B_5'),
            Stat('_autoCommunity_B_6'),
            Stat('_autoCommunity_B_7'),
            Stat('_autoCommunity_B_8'),

            Stat('_teleopCommunity_T_0'),
            Stat('_teleopCommunity_T_1'),
            Stat('_teleopCommunity_T_2'),
            Stat('_teleopCommunity_T_3'),
            Stat('_teleopCommunity_T_4'),
            Stat('_teleopCommunity_T_5'),
            Stat('_teleopCommunity_T_6'),
            Stat('_teleopCommunity_T_7'),
            Stat('_teleopCommunity_T_8'),

            Stat('_teleopCommunity_M_0'),
            Stat('_teleopCommunity_M_1'),
            Stat('_teleopCommunity_M_2'),
            Stat('_teleopCommunity_M_3'),
            Stat('_teleopCommunity_M_4'),
            Stat('_teleopCommunity_M_5'),
            Stat('_teleopCommunity_M_6'),
            Stat('_teleopCommunity_M_7'),
            Stat('_teleopCommunity_M_8'),

            Stat('_teleopCommunity_B_0'),
            Stat('_teleopCommunity_B_1'),
            Stat('_teleopCommunity_B_2'),
            Stat('_teleopCommunity_B_3'),
            Stat('_teleopCommunity_B_4'),
            Stat('_teleopCommunity_B_5'),
            Stat('_teleopCommunity_B_6'),
            Stat('_teleopCommunity_B_7'),
            Stat('_teleopCommunity_B_8'),

            # Create Linked Stats
            LinkedStat('mobility','mobilityRobot', {"Yes":3,"No":0}),
            LinkedStat('autoChargeStation','autoChargeStationRobot', {"Engaged":12,"Docked":8,"None":0}),
            LinkedStat('endGameChargeStation','endGameChargeStationRobot', {"Docked":10,"Park":2, "None": 0}),

            # Aggregate Stats Based upon Placement Position and Type
            SumStat('autoHighCubes',[
                '_autoCommunity_T_1',
                '_autoCommunity_T_4',
                '_autoCommunity_T_7'
            ]),

            SumStat('autoHighCones',[
                '_autoCommunity_T_0',
                '_autoCommunity_T_2',
                '_autoCommunity_T_3',
                '_autoCommunity_T_5',
                '_autoCommunity_T_6',
                '_autoCommunity_T_8',
            ]),

            SumStat('autoMidCubes',[
                '_autoCommunity_M_1',
                '_autoCommunity_M_4',
                '_autoCommunity_M_7'
            ]),

            SumStat('autoMidCones',[
                '_autoCommunity_M_0',
                '_autoCommunity_M_2',
                '_autoCommunity_M_3',
                '_autoCommunity_M_5',
                '_autoCommunity_M_6',
                '_autoCommunity_M_8',
            ]),

            SumStat('autoLow',[
                '_autoCommunity_B_0',
                '_autoCommunity_B_1',
                '_autoCommunity_B_2',
                '_autoCommunity_B_3',
                '_autoCommunity_B_4',
                '_autoCommunity_B_5',
                '_autoCommunity_B_6',
                '_autoCommunity_B_7',
                '_autoCommunity_B_8',
            ]),

            SumStat('teleopHighCubes',[
                '_teleopCommunity_T_1',
                '_teleopCommunity_T_4',
                '_teleopCommunity_T_7'
            ]),

            SumStat('teleopHighCones',[
                '_teleopCommunity_T_0',
                '_teleopCommunity_T_2',
                '_teleopCommunity_T_3',
                '_teleopCommunity_T_5',
                '_teleopCommunity_T_6',
                '_teleopCommunity_T_8',
            ]),

            SumStat('teleopMidCubes',[
                '_teleopCommunity_M_1',
                '_teleopCommunity_M_4',
                '_teleopCommunity_M_7'
            ]),

            SumStat('teleopMidCones',[
                '_teleopCommunity_M_0',
                '_teleopCommunity_M_2',
                '_teleopCommunity_M_3',
                '_teleopCommunity_M_5',
                '_teleopCommunity_M_6',
                '_teleopCommunity_M_8',
            ]),

            SumStat('teleopLow',[
                '_teleopCommunity_B_0',
                '_teleopCommunity_B_1',
                '_teleopCommunity_B_2',
                '_teleopCommunity_B_3',
                '_teleopCommunity_B_4',
                '_teleopCommunity_B_5',
                '_teleopCommunity_B_6',
                '_teleopCommunity_B_7',
                '_teleopCommunity_B_8',
            ]),
            SumStat('elementsScored',[
                'teleopLow',
                'teleopMidCubes',
                'teleopMidCones',
                'teleopHighCubes',
                'teleopHighCones',
                'autoLow',
                'autoMidCubes',
                'autoMidCones',
                'autoHighCubes',
                'autoMidCones',
            ]),
            CustomStat('links', self.calc_links),
            SumStat('linkPoints',['links'],display_name="Links", weights = [5], report_stat = True),

            SumStat('autoPoints',[
                'autoHighCubes',
                'autoHighCones',
                'autoMidCubes',
                'autoMidCones',
                'autoLow',
                'mobility',
                'autoChargeStation'
            ], weights = [
                6,6,4,4,3,1,1
            ],display_name="Auto", report_stat = True),

            SumStat('teleopPoints',[
                'teleopHighCubes',
                'teleopHighCones',
                'teleopMidCubes',
                'teleopMidCones',
                'teleopLow',
            ], weights = [
                5,5,3,3,2
            ],display_name="Teleop", report_stat = True),

            

            

            SumStat('endgamePoints',[
                'endGameChargeStation'
            ],display_name="End Game", report_stat = True),

            SumStat('OPR',[
                'teleopPoints',
                'autoPoints',
                'endgamePoints',
                'linkPoints'
            ], display_name="OPR", report_stat = True),

            SumStat('simulatedRanking',[]),
            # SumStat('expectedRanking',[], display_name='Expected Ranking', report_stat = True),
            CustomStat('schedule', self.calc_schedule, display_name='Schedule', report_stat = True)
            

            
            

            
            # LinkedStat('autoChargeStation','autoCharageStationRobot', {"Yes":2,"None":0}),
            
            
        ]

    def flatten_arrays(self, played_matches:list, teams:dict):
        for match in played_matches:
            for color in ['blue','red']:
                for gamemode_key in ['autoCommunity','teleopCommunity']:
                    for top_middle_bottom in ['B','M','T']:
                        score_array = match.get('score_breakdown',{}).get(color,{}).get(gamemode_key,{}).get(top_middle_bottom,[])
                        for index, elem in enumerate(score_array):
                            value = 0 
                            if elem != "None":
                                value = 1
                            else:
                                value = 0

                            match['score_breakdown'][color][f'_{gamemode_key}_{top_middle_bottom}_{index}'] = value
        
                color_performance = match.get('score_breakdown',{}).get(color,{})
                if color_performance.get('autoBridgeState','Level') == 'Level':
                    for i in range(0,3):
                        if color_performance.get(f'autoChargeStationRobot{i}') == 'Docked':
                            match['score_breakdown'][color][f'autoChargeStationRobot{index}'] = 'Engaged'
                        
        # print("\n\n\n====================\n\n\n", played_matches)
        return played_matches, teams

    # Computes Auto Charging Station points allocations
    def calc_links(self, played_matches:list, teams:list, stat:dict, rankings:dict)-> dict:
        
        for team in teams:
            stats = teams[team]
            
            high_links = float(min(stats.get('teleopHighCubes',0) + stats.get('autoHighCubes'), (stats.get('teleopHighCones',0) + stats.get('autoHighCubes'))/2.0))
            mid_links = float(min(stats.get('teleopMidCubes',0) + stats.get('autoMidCubes'), (stats.get('teleopMidCones',0) + stats.get('autoMidCubes'))/2.0))
            low_links = float(stats.get('teleopLow') + stats.get('autoLow'))/3.0

            stats['links'] = high_links + mid_links + low_links
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
        ranks = {}
        for team in teams:
            ranks[team] = []

        num_sims = 1000
        for i in range(0,num_sims):
            simulated_schedules = get_random_schedule(teams, len(matches))
            simulated_rps = simulate_event(simulated_schedules, teams, self.predict_match, self.parse_rps)
            rankings = sorted(simulated_rps.items(), key=lambda x:x[1], reverse = True)
            rank = 1
            for team in rankings:
                ranks[team[0]].append(rank)
                rank +=1
        
        ranks = sorted(ranks.items(), key=lambda x:sum(x[1]))
        count = 1
        for rank in ranks:
            teams[rank[0]]['simulatedRanking'] = count
            count +=1

        
        expected_rp = simulate_event(matches, teams, self.predict_match, self.parse_rps)
        rankings = sorted(expected_rp.items(), key=lambda x:x[1], reverse = True)
        
        count = 1
        for rank in rankings:
            teams[rank[0]]['expectedRanking'] = count
            teams[rank[0]]['schedule'] = teams[rank[0]]['simulatedRanking'] - count
            count +=1

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
        for team_key in match.get('alliances',{}).get(color,{}).get('team_keys',[]):
            team = teams.get(team_key,{})
            auto_elements += team.get('autoHighCubes',0) + team.get('autoHighCones',0) + team.get('autoMidCubes',0) + team.get('autoMidCones',0) + team.get('autoLow',0)
            high_cubes += team.get('autoHighCubes',0) + team.get('teleopHighCubes',0)
            high_cones += team.get('autoHighCones',0) + team.get('teleopHighCones',0)

            mid_cubes += team.get('autoMidCubes',0) + team.get('teleopMidCubes',0)
            mid_cubes += team.get('autoMidCones',0) + team.get('teleopMidCones',0)

            low += team.get('autoLow',0) + team.get('teleopLow',0)
            endgame += team.get('endgamePoints',0)
            auto_charge_station = max(auto_charge_station, team.get('autoChargeStation',0))

        


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
            low = 9

        high_links = int(min(high_cubes, high_cones / 2.0))
        mid_links = int(min(mid_cubes, mid_cones / 2.0))
        low_links = int(low / 3.0)

        links = high_links + mid_links + low_links

        score = links * 5 + (high_cubes + high_cones) * 5 + (mid_cubes + mid_cones) * 3 + low * 2 + auto_elements + auto_charge_station + endgame

        prediction[f"{color}_teams"] = match.get('alliances',{}).get(color,{}).get('team_keys',[])
        prediction[f"{color}_score"] = round(score,2)
        prediction[f"{color}_highCubes"] = round(high_cubes,2)
        prediction[f"{color}_highCubes"] = round(high_cones,2)
        prediction[f"{color}_midCubes"] = round(mid_cubes,2)
        prediction[f"{color}_midCones"] = round(mid_cones,2)
        prediction[f"{color}_low"] = round(low,2)
        prediction[f"{color}_links"] = round(links,2)
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

        if prediction['blue_links'] > 5:
            prediction['blue_link_rp'] = 1
        else:
            prediction['blue_link_rp'] = 0

        if prediction['red_links'] > 5:
            prediction['red_link_rp'] = 1
        else:
            prediction['red_link_rp'] = 0

        # print(match.get('score_breakdown',{}).get('blue',{}).get('totalPoints',0) - match.get('score_breakdown',{}).get('blue',{}).get('foulPoints',0), prediction.get('blue_score'))
        return prediction
    
    def parse_rps(self, match:dict) -> tuple:
        blue_rp = 0
        red_rp = 0
        
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('activationBonusAchieved'))
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('sustainabilityBonusAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('activationBonusAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('sustainabilityBonusAchieved'))

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