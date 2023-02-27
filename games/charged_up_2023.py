from games.frc_game import FRCGame
from analysis.stat import Stat, LinkedStat, SumStat, CustomStat



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

            CustomStat('links', self.calc_links),
            SumStat('linkPoints',['links'], weights = [5], report_stat = True),

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

            


            
            

            
            # LinkedStat('autoChargeStation','autoCharageStationRobot', {"Yes":2,"None":0}),
            
            
        ]

        self.rp_functions = [
            self.get_link_rp,
            self.get_charge_rp,
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
            
            high_links = int(float(min(stats.get('teleopHighCubes',0) + stats.get('autoHighCubes'), (stats.get('teleopHighCones',0) + stats.get('autoHighCubes'))/2.0)))
            mid_links = int(float(min(stats.get('teleopMidCubes',0) + stats.get('autoMidCubes'), (stats.get('teleopMidCones',0) + stats.get('autoMidCubes'))/2.0)))
            low_links = int(float(stats.get('teleopLow') + stats.get('autoLow'))/3.0)

            stats['links'] = high_links + mid_links + low_links
        return teams
        

    # Assigns Event Rankings to all the Teams at the event
    def assign_ranks(self, played_matches:list, teams:list, stat:dict, rankings:dict)-> dict:
        for rank in rankings['rankings']:
            teams[rank['team_key']]['rank'] = rank['rank']
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
            auto_elements += team.get('autoHighCubes') + team.get('autoHighCones') + team.get('autoMidCubes') + team.get('autoMidCones') + team.get('autoLow')
            high_cubes += team.get('autoHighCubes') + team.get('teleopHighCubes')
            high_cones += team.get('autoHighCones') + team.get('teleopHighCones')

            mid_cubes += team.get('autoMidCubes') + team.get('teleopMidCubes')
            mid_cubes += team.get('autoMidCones') + team.get('teleopMidCones')

            low += team.get('autoLow') + team.get('teleopLow')
            endgame += team.get('endgamePoints')
            auto_charge_station = max(auto_charge_station, team.get('autoChargeStation'))

        


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

        


    def predict_match(self, match:dict, teams:dict) -> dict:
        #print("Predicting Match", match)
        prediction = {
            'comp_level': match.get('comp_level', 'unknown'),
            'key': match.get('key', 'unknown'),
            'match_number': match.get('match_number',0),
        }

        self.predict_alliance('blue', match, teams, prediction)
        self.predict_alliance('red', match, teams, prediction)

        # print(match.get('score_breakdown',{}).get('blue',{}).get('totalPoints',0) - match.get('score_breakdown',{}).get('blue',{}).get('foulPoints',0), prediction.get('blue_score'))
        return prediction

         


    def get_link_rp(self, match:dict) -> tuple:
        return (0,0)

    def get_charge_rp(self, match:dict) -> tuple:
        return (0,0)
