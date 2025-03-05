from games.frc_game import FRCGame
from analysis.stat import Stat, LinkedStat, SumStat, CustomStat, PostStat
from analysis.simulator import get_random_schedule, simulate_event, get_clean_schedule, get_qual_matches
from analysis.chart import Chart, ChartField
import numpy as np

class Reefscape2025(FRCGame):
    def __init__(self):

        self.preprocessors = [
            self.flatten_arrays,
            self.adjust_algae
        ]

        self.stats = [
            CustomStat('rank', self.assign_ranks, report_stat=True, display_name='Rank'),

            # Declare all Source Stats
            Stat('_autoReef_topRow_0'),
            Stat('_autoReef_topRow_1'),
            Stat('_autoReef_topRow_2'),
            Stat('_autoReef_topRow_3'),
            Stat('_autoReef_topRow_4'),
            Stat('_autoReef_topRow_5'),
            Stat('_autoReef_topRow_6'),
            Stat('_autoReef_topRow_7'),
            Stat('_autoReef_topRow_8'),
            Stat('_autoReef_topRow_9'),
            Stat('_autoReef_topRow_10'),
            Stat('_autoReef_topRow_11'),
            
            Stat('_autoReef_midRow_0'),
            Stat('_autoReef_midRow_1'),
            Stat('_autoReef_midRow_2'),
            Stat('_autoReef_midRow_3'),
            Stat('_autoReef_midRow_4'),
            Stat('_autoReef_midRow_5'),
            Stat('_autoReef_midRow_6'),
            Stat('_autoReef_midRow_7'),
            Stat('_autoReef_midRow_8'),
            Stat('_autoReef_midRow_9'),
            Stat('_autoReef_midRow_10'),
            Stat('_autoReef_midRow_11'),

            Stat('_autoReef_botRow_0'),
            Stat('_autoReef_botRow_1'),
            Stat('_autoReef_botRow_2'),
            Stat('_autoReef_botRow_3'),
            Stat('_autoReef_botRow_4'),
            Stat('_autoReef_botRow_5'),
            Stat('_autoReef_botRow_6'),
            Stat('_autoReef_botRow_7'),
            Stat('_autoReef_botRow_8'),
            Stat('_autoReef_botRow_9'),
            Stat('_autoReef_botRow_10'),
            Stat('_autoReef_botRow_11'),

            Stat('_autoReef_trough'),


            Stat('_teleopReef_topRow_0'),
            Stat('_teleopReef_topRow_1'),
            Stat('_teleopReef_topRow_2'),
            Stat('_teleopReef_topRow_3'),
            Stat('_teleopReef_topRow_4'),
            Stat('_teleopReef_topRow_5'),
            Stat('_teleopReef_topRow_6'),
            Stat('_teleopReef_topRow_7'),
            Stat('_teleopReef_topRow_8'),
            Stat('_teleopReef_topRow_9'),
            Stat('_teleopReef_topRow_10'),
            Stat('_teleopReef_topRow_11'),
            
            Stat('_teleopReef_midRow_0'),
            Stat('_teleopReef_midRow_1'),
            Stat('_teleopReef_midRow_2'),
            Stat('_teleopReef_midRow_3'),
            Stat('_teleopReef_midRow_4'),
            Stat('_teleopReef_midRow_5'),
            Stat('_teleopReef_midRow_6'),
            Stat('_teleopReef_midRow_7'),
            Stat('_teleopReef_midRow_8'),
            Stat('_teleopReef_midRow_9'),
            Stat('_teleopReef_midRow_10'),
            Stat('_teleopReef_midRow_11'),

            Stat('_teleopReef_botRow_0'),
            Stat('_teleopReef_botRow_1'),
            Stat('_teleopReef_botRow_2'),
            Stat('_teleopReef_botRow_3'),
            Stat('_teleopReef_botRow_4'),
            Stat('_teleopReef_botRow_5'),
            Stat('_teleopReef_botRow_6'),
            Stat('_teleopReef_botRow_7'),
            Stat('_teleopReef_botRow_8'),
            Stat('_teleopReef_botRow_9'),
            Stat('_teleopReef_botRow_10'),
            Stat('_teleopReef_botRow_11'),

            Stat('_teleopReef_trough'),

            Stat('_teamNetAlgae'), # Preprocessed to be represent the number of algae the team scored in the net. Ignoring how many the opponent scored in the processor
            Stat('wallAlgaeCount'),

            # Create Linked Stats
            LinkedStat('autoLine','autoLineRobot', {"Yes":3,"No":0}),
            LinkedStat('endGameBarge','endGameRobot', {"DeepCage":12,"ShallowCage":6, "Parked": 2}),

            # Aggregate Stats Based upon Placement Position and Type
            SumStat('autoL4Corral',[
                '_autoReef_topRow_0',
                '_autoReef_topRow_1',
                '_autoReef_topRow_2',
                '_autoReef_topRow_3',
                '_autoReef_topRow_4',
                '_autoReef_topRow_5',
                '_autoReef_topRow_6',
                '_autoReef_topRow_7',
                '_autoReef_topRow_8',
                '_autoReef_topRow_9',
                '_autoReef_topRow_10',
                '_autoReef_topRow_11',
            ]),

            SumStat('autoL3Corral',[
                '_autoReef_midRow_0',
                '_autoReef_midRow_1',
                '_autoReef_midRow_2',
                '_autoReef_midRow_3',
                '_autoReef_midRow_4',
                '_autoReef_midRow_5',
                '_autoReef_midRow_6',
                '_autoReef_midRow_7',
                '_autoReef_midRow_8',
                '_autoReef_midRow_9',
                '_autoReef_midRow_10',
                '_autoReef_midRow_11',
            ]),

            SumStat('autoL2Corral',[
                '_autoReef_botRow_0',
                '_autoReef_botRow_1',
                '_autoReef_botRow_2',
                '_autoReef_botRow_3',
                '_autoReef_botRow_4',
                '_autoReef_botRow_5',
                '_autoReef_botRow_6',
                '_autoReef_botRow_7',
                '_autoReef_botRow_8',
                '_autoReef_botRow_9',
                '_autoReef_botRow_10',
                '_autoReef_botRow_11',
            ]),

            

            SumStat('teleopL4Corral',[
                '_teleopReef_topRow_0',
                '_teleopReef_topRow_1',
                '_teleopReef_topRow_2',
                '_teleopReef_topRow_3',
                '_teleopReef_topRow_4',
                '_teleopReef_topRow_5',
                '_teleopReef_topRow_6',
                '_teleopReef_topRow_7',
                '_teleopReef_topRow_8',
                '_teleopReef_topRow_9',
                '_teleopReef_topRow_10',
                '_teleopReef_topRow_11',
            ]),

            SumStat('teleopL3Corral',[
                '_teleopReef_midRow_0',
                '_teleopReef_midRow_1',
                '_teleopReef_midRow_2',
                '_teleopReef_midRow_3',
                '_teleopReef_midRow_4',
                '_teleopReef_midRow_5',
                '_teleopReef_midRow_6',
                '_teleopReef_midRow_7',
                '_teleopReef_midRow_8',
                '_teleopReef_midRow_9',
                '_teleopReef_midRow_10',
                '_teleopReef_midRow_11',
            ]),

            SumStat('teleopL2Corral',[
                '_teleopReef_botRow_0',
                '_teleopReef_botRow_1',
                '_teleopReef_botRow_2',
                '_teleopReef_botRow_3',
                '_teleopReef_botRow_4',
                '_teleopReef_botRow_5',
                '_teleopReef_botRow_6',
                '_teleopReef_botRow_7',
                '_teleopReef_botRow_8',
                '_teleopReef_botRow_9',
                '_teleopReef_botRow_10',
                '_teleopReef_botRow_11',
            ]),

            SumStat('autoCorralScored',[
                'autoL4Corral',
                'autoL3Corral',
                'autoL2Corral',
                '_autoReef_trough',
            ]),
            
            SumStat('teleopCorralScored',[
                'teleopL4Corral',
                'teleopL3Corral',
                'teleopL2Corral',
                '_teleopReef_trough',
            ]),

            SumStat('l4CorralScored',[
                'autoL4Corral',
                'teleopL4Corral',
            ]),

            SumStat('l3CorralScored',[
                'autoL3Corral',
                'teleopL3Corral',
            ]),

            SumStat('l2CorralScored',[
                'autoL2Corral',
                'teleopL2Corral',
            ]),

            SumStat('l1CorralScored',[
                '_autoReef_trough',
                '_teleopReef_trough',
            ]),

            SumStat('teleopElementsScored',[
                'teleopCorralScored',
                '_teamNetAlgae',
                'wallAlgaeCount',
            ]),            

            SumStat('totalCoralScored',[
                'autoCorralScored',
                'teleopCorralScored',
            ], report_stat = True, display_name="Coral"),

            SumStat('totalAlgaeScored',[
                '_teamNetAlgae',
                'wallAlgaeCount',
            ], report_stat = True, display_name="Algae"),

            SumStat('autoPoints',[
                'autoL4Corral',
                'autoL3Corral',
                'autoL2Corral',
                '_autoReef_trough',
                'autoLine',
            ], weights = [
                7,6,4,3,3
            ],display_name="Auto", report_stat = True),

            SumStat('teleopPoints',[
                'teleopL4Corral',
                'teleopL3Corral',
                'teleopL2Corral',
                '_teleopReef_trough',
                '_teamNetAlgae',
                'wallAlgaeCount'
            ], weights = [
                5,4,3,2,4,2
            ],display_name="Teleop", report_stat = True),


            SumStat('endgamePoints',[
                'endGameBarge'
            ],display_name="End Game", report_stat = True),

            SumStat('OPR',[
                'teleopPoints',
                'autoPoints',
                'endgamePoints'
            ], display_name="OPR", report_stat = True),

            SumStat('simulatedRanking',[]),
            SumStat('expectedRanking',[], display_name='Expected Ranking', report_stat = True),
            PostStat('schedule', self.calc_schedule, display_name='Schedule', report_stat = True)
            

            
            

            
            # LinkedStat('autoChargeStation','autoCharageStationRobot', {"Yes":2,"None":0}),
            
            
        ]
        
        self.charts = [
            Chart('OPR', [
                ChartField('teleopPoints', display_text='Teleop'),
                ChartField('autoPoints', display_text='Auto'),
                ChartField('endgamePoints', display_text='EndGame')],
            ),
            Chart('Corral Scoring Location', [
                ChartField('l4CorralScored', display_text='L4'),
                ChartField('l3CorralScored', display_text='L3'),
                ChartField('l2CorralScored', display_text='L2'),
                ChartField('l1CorralScored', display_text='L1'),
                ],
            ),
            Chart('Algae Scoring Location', [
                ChartField('_teamNetAlgae', display_text='Net'),
                ChartField('wallAlgaeCount', display_text='Processor'),
                ],
            ),
            Chart('Elements Scoring Period', [
                ChartField('autoCorralScored', display_text='Auto'),
                ChartField('teleopElementsScored', display_text='Teleop')],
            ),
            Chart('Elements Scoring Type', [
                ChartField('totalCoralScored', display_text='Corral'),
                ChartField('totalAlgaeScored', display_text='Algae')],
            ),
        ]

    def flatten_arrays(self, played_matches:list, teams:dict):
        for match in played_matches:
            for color in ['blue','red']:
                # for gamemode_key in ['autoReef','teleopReef']:
                for top_middle_bottom in ['botRow','midRow','topRow']:
                    teleop_score_array = match.get('score_breakdown',{}).get(color,{}).get('teleopReef',{}).get(top_middle_bottom,[])
                    auto_score_array = match.get('score_breakdown',{}).get(color,{}).get('autoReef',{}).get(top_middle_bottom,[])
                    for index, (teleop_elem, auto_elem) in enumerate(zip(teleop_score_array, auto_score_array)):
                        auto_value = 0
                        teleop_value = 0

                        if auto_score_array[auto_elem]:
                            auto_value = 1
                        elif teleop_score_array[teleop_elem]:
                            teleop_value = 1
                        
                        match['score_breakdown'][color][f'_autoReef_{top_middle_bottom}_{index}'] = auto_value
                        match['score_breakdown'][color][f'_teleopReef_{top_middle_bottom}_{index}'] = teleop_value

                match['score_breakdown'][color][f'_autoReef_trough'] = match.get('score_breakdown',{}).get(color,{}).get('autoReef',{}).get("trough",0)
                match['score_breakdown'][color][f'_teleopReef_trough'] = max(match.get('score_breakdown',{}).get(color,{}).get('teleopReef',{}).get("trough",0) - match['score_breakdown'][color][f'_autoReef_trough'],0)
        return played_matches, teams

    def adjust_algae(self, played_matches:list, teams:dict):
        for match in played_matches:
            red_processor_algae = match.get('score_breakdown',{}).get('red',{}).get('wallAlgaeCount',0)
            blue_processor_algae = match.get('score_breakdown',{}).get('blue',{}).get('wallAlgaeCount',0)

            red_total_net_algae = match.get('score_breakdown',{}).get('red',{}).get('netAlgaeCount',0)
            blue_total_net_algae = match.get('score_breakdown',{}).get('blue',{}).get('netAlgaeCount',0)

            match['score_breakdown']['red'][f'_teamNetAlgae'] = max(blue_total_net_algae - red_processor_algae,0)
            match['score_breakdown']['blue'][f'_teamNetAlgae'] = max(red_total_net_algae - blue_processor_algae,0)

        return played_matches, teams

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
            schedule_adjust += expected_rp[rank[0]] / (sum(rps[rank[0]]) / num_sims)
            count +=1

        
        schedule_adjust = schedule_adjust / (len(ranks))

        count = 1
        avg_percentile = 0

        for rank in rankings:
            teams[rank[0]]['expectedRanking'] = count
            rp_distribution = sorted(rps[rank[0]])
            # lb = np.searchsorted(rp_distribution, expected_rp)
            percentile = (np.searchsorted(rp_distribution, expected_rp[rank[0]], side="left")) / num_sims * 100

            teams[rank[0]]['schedule'] = percentile
            avg_percentile += percentile
            count +=1
            
        return teams

    def validate_match(self, match:dict) -> bool:
        return True

    def predict_alliances(self, match:dict, teams:dict, prediction:dict):


        for color in ['red', 'blue']:

            auto_points = 0
            teleop_points = 0

            autoL4Corral = 0
            autoL3Corral = 0
            autoL2Corral = 0
            autoL1Corral = 0

            teleopL4Corral = 0
            teleopL3Corral = 0
            teleopL2Corral = 0
            teleopL1Corral = 0

            totalL4Corral = 0
            totalL3Corral = 0
            totalL2Corral = 0
            totalL1Corral = 0

            autoLeave = 0
            barge = 0

            processorAlgae = 0
            netAlgae = 0

            for team_key in match.get('alliances',{}).get(color,{}).get('team_keys',[]):
                team = teams.get(team_key,{})

                autoL4Corral += team.get('autoL4Corral',0)
                autoL3Corral += team.get('autoL3Corral',0)
                autoL2Corral += team.get('autoL2Corral',0)
                autoL1Corral += team.get('_autoReef_trough',0)

                teleopL4Corral += team.get('teleopL4Corral',0)
                teleopL3Corral += team.get('teleopL3Corral',0)
                teleopL2Corral += team.get('teleopL2Corral',0)
                teleopL1Corral += team.get('_teleopReef_trough',0)

                barge += team.get('endGameBarge',0)
                autoLeave += team.get('autoLine',0)

                netAlgae += float(team.get("_teamNetAlgae"))
                processorAlgae += float(team.get('wallAlgaeCount'))


            totalL4Corral = autoL4Corral + teleopL4Corral
            if totalL4Corral > 12:
                totalL3Corral = totalL4Corral - 12
                totalL4Corral = 12
            
            totalL3Corral += autoL3Corral + teleopL3Corral
            if totalL3Corral > 12:
                totalL2Corral = totalL3Corral - 12
                totalL3Corral = 12

            totalL2Corral += autoL2Corral + teleopL2Corral
            if totalL2Corral > 12:
                totalL1Corral = totalL2Corral - 12
                totalL2Corral = 12

            totalL1Corral += autoL1Corral + teleopL1Corral


            score = round(autoL4Corral) * 7 + round(autoL3Corral) * 6 + round(autoL2Corral) * 4 + round(autoL1Corral) * 3 + round(teleopL4Corral) * 5 + round(teleopL3Corral) * 4 + round(teleopL2Corral) * 3 + round(teleopL1Corral) * 2 + autoLeave + barge + 4 * round(netAlgae) + 6 * round(processorAlgae)

            prediction[f"{color}_teams"] = match.get('alliances',{}).get(color,{}).get('team_keys',[])
            prediction[f"{color}_score"] = score
            prediction[f"{color}_l4Corral"] = round(totalL4Corral,2)
            prediction[f"{color}_l3Corral"] = round(totalL3Corral,2)
            prediction[f"{color}_l2Corral"] = round(totalL2Corral,2)
            prediction[f"{color}_l1Corral"] = round(totalL1Corral,2)
            prediction[f"{color}_processorAlgae"] = round(processorAlgae,2)
            prediction[f"{color}_autoLeave"] = round(autoLeave,2)
            prediction[f"{color}_endGameBarge"] = round(barge,2)

        prediction["red_score"] = round(prediction["red_score"] + 4 * round(prediction["blue_processorAlgae"]),2)
        prediction["blue_score"] = round(prediction["blue_score"] + 4 * round(prediction["red_processorAlgae"]),2)

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

        self.predict_alliances(match, teams, prediction)
        

        
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


        # Assign RP for Achiving the Coral RP
        coopertition = prediction['red_processorAlgae'] >= 2 and prediction['blue_processorAlgae'] >=2
        blue_levels = int(prediction['blue_l4Corral'] >= 5) + int(prediction['blue_l3Corral'] >= 5) + int(prediction['blue_l2Corral'] >= 5) + int(prediction['blue_l1Corral']>= 5)
        red_levels = int(prediction['red_l4Corral']>= 5) + int(prediction['red_l3Corral'] >= 5) + int(prediction['red_l2Corral'] >= 5) + int(prediction['red_l1Corral'] >= 5)

        if coopertition:
            if blue_levels >=3:
                prediction['blue_corral_rp'] = 1
            else:
                prediction['blue_corral_rp'] = 0

            if red_levels >=3:
                prediction['red_corral_rp'] = 1
            else:
                prediction['red_corral_rp'] = 0
        else:
            if blue_levels >=4:
                prediction['blue_corral_rp'] = 1
            else:
                prediction['blue_corral_rp'] = 0

            if red_levels >=4:
                prediction['red_corral_rp'] = 1
            else:
                prediction['red_corral_rp'] = 0

        # Assign RP for Achiving the Auto RP
        if prediction['blue_autoLeave'] >= 7:
            prediction['blue_auto_rp'] =1
        else:
            prediction['blue_auto_rp'] =0

        if prediction['red_autoLeave'] >= 7:
            prediction['red_auto_rp'] =1
        else:
            prediction['red_auto_rp'] =0

        # Assign RP for Achieving the Climb RP
        if prediction['blue_endGameBarge'] >= 7:
            prediction['blue_barge_rp'] =1
        else:
            prediction['blue_barge_rp'] =0

        if prediction['red_endGameBarge'] >= 7:
            prediction['red_barge_rp'] =1
        else:
            prediction['red_barge_rp'] =0

        return prediction
    
    def parse_rps(self, match:dict) -> tuple:
        blue_rp = 0
        red_rp = 0
        
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('bargeBonusAchieved'))
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('coralBonusAchieved'))
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('autoBonusAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('bargeBonusAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('coralBonusAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('autoBonusAchieved'))


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

    def validate_match(self, match:dict) -> bool:
        passing = True
        passing = 'frc0' not in match.get('alliances',{}).get('blue',{}).get('team_keys',[]) and passing
        passing = 'frc0' not in match.get('alliances',{}).get('red',{}).get('team_keys',[]) and passing
        return passing
