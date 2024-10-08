from games.frc_game import FRCGame
from analysis.stat import Stat, LinkedStat, SumStat, CustomStat, PostStat
from analysis.simulator import get_random_schedule, simulate_event, get_clean_schedule, get_qual_matches
from analysis.chart import Chart, ChartField
from scipy.optimize import nnls
import numpy as np

class Crescendo2024(FRCGame):
    def __init__(self):

        self.preprocessors = [
        ]

        self.stats = [
            CustomStat('rank', self.assign_ranks, display_name = 'Rank', report_stat=True, order = 1),

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
            ], display_name="Auto", weights = [2,1,5], report_stat = True, order = 4),

            SumStat('teleopPoints',[
                'teleopSpeakerNoteAmplifiedCount',
                'teleopSpeakerNoteCount',
                'teleopAmpNoteCount',
            ], weights = [
                5,2,1
            ],
            display_name="Teleop", report_stat = True, order=5),

            SumStat('endgamePoints',[
                'climb',
                'trapNoteCount',
            ], 
            weights = [1,5],
            display_name="End Game", report_stat = True, order=6),


            SumStat('noteCount',[
                'trapNoteCount',
                'autoAmpNoteCount',
                'autoSpeakerNoteCount',
                'teleopAmpNoteCount',
                'teleopSpeakerNoteCount',
                'teleopSpeakerNoteAmplifiedCount'
            ], report_stat = True, display_name = 'Notes', order=2),
            
            SumStat('ampNoteCount',[
                'autoAmpNoteCount',
                'teleopAmpNoteCount',
            ], report_stat = False, display_name="Amp Notes"),
            
            SumStat('speakerNoteCount',[
                'autoSpeakerNoteCount',
                'teleopSpeakerNoteCount',
            ], report_stat = False, display_name="Speaker Notes"),

            SumStat('autoNoteCount',[
                'autoAmpNoteCount',
                'autoSpeakerNoteCount',
            ], report_stat = False, display_name="Auto Notes"),
            
            SumStat('teleopNoteCount',[
                'teleopAmpNoteCount',
                'teleopSpeakerNoteCount',
            ], report_stat = False, display_name="Teleop Notes"),
            

            SumStat('OPR',[
                'teleopPoints',
                'autoPoints',
                'endgamePoints'
            ], display_name="OPR", report_stat = True, order=0),

            # 
            SumStat('simulatedRanking',[]),
            SumStat('expectedRanking',[], display_name='Expected Ranking', report_stat = True,order=7),
            PostStat('schedule', self.calc_schedule, display_name='Schedule', report_stat = True, order =8)
            
            
            
        ]

        self.charts = [
            Chart('OPR', [
                ChartField('teleopPoints', display_text='Teleop'),
                ChartField('autoPoints', display_text='Auto'),
                ChartField('endgamePoints', display_text='EndGame')],
            ),
            Chart('Elements Scoring Location', [
                ChartField('ampNoteCount', display_text='Amp'),
                ChartField('speakerNoteCount', display_text='Speaker'),
                ChartField('trapNoteCount', display_text='Trap')],
            ),
            Chart('Elements Scoring Period', [
                ChartField('autoNoteCount', display_text='Auto'),
                ChartField('teleopNoteCount', display_text='Teleop'),
                ChartField('trapNoteCount', display_text='EndGame')],
            ),
        ]
        # 'Elements Scoring Period', [
                # ChartField('teleopPoints', display_text='Teleop'),
                # ChartField('autoPoints', display_text='Auto'),
                # ChartField('endgamePoints', display_text='EndGame')],

  
    # Performs best guess calculations on who is scoring each trap each match
    def calc_trap_notes(self, played_matches:list, teams:list, stat:dict, rankings:dict) -> dict:
        num_matches = len(played_matches)
        num_teams = len(teams)
        team_array = np.zeros([num_matches*6, num_teams])
        score_array = np.zeros(num_matches*6)

        team_traps = {}
        ambiguous_traps = 0
        num_traps = 0

        for (i, match) in enumerate(played_matches):
            for color in ['red', 'blue']:
                # team_climb_mapping = {}
                score = match.get('score_breakdown',{}).get(color,{})

                team_keys = match.get('alliances',{}).get(color, {}).get('team_keys',[])
                trapKeys = ['trapCenterStage', 'trapStageLeft', 'trapStageRight']

                
                for (j, trapKey) in enumerate(trapKeys):
                    if score.get(trapKey, False):
                        
                        num_traps +=1
                        offset = 0
                        if color == 'red':
                            offset = num_matches*3

                        # Setup Score Array
                        score_array[int(offset + i*3 + j)] = 1

                        # Get the List of Teams who could have scored that trap
                        possible_traps = self.get_possible_teams_for_trap(trapKey, color, match)

                        if len(possible_traps) != 1:
                            ambiguous_traps +=1
                        else:
                            if possible_traps[0] in team_traps:
                                team_traps[possible_traps[0]] += 1
                            else:
                                team_traps[possible_traps[0]] = 1

                        #
                        possible_traps = team_keys
                        for team_key in possible_traps:
                            team_index = teams[team_key]['_index']
                            team_array[offset + i*3 + j][team_index] = 1                            
        
        if num_matches > 0:
            if ambiguous_traps <= num_traps / 2:
                for i, team in enumerate(teams.values()):
                    if team['key'] in team_traps:
                        team['trapNoteCount'] = team_traps[team['key']] / len(team['_autoLinePoints_list'])
                    else:
                        team['trapNoteCount'] = 0
            else:
                X = nnls(team_array,score_array)[0]
                for i, team in enumerate(teams.values()):
                    team['trapNoteCount'] = X[team["_index"]]
        else:
            for i, team in enumerate(teams.values()):
                team['trapNoteCount'] = 0

        
        
        return teams

    

    def get_possible_teams_for_trap(self, trapKey: str, color: str, match:dict) -> list:
        team_keys = match.get('alliances',{}).get(color, {}).get('team_keys',[])
        score = match.get('score_breakdown',{}).get(color,{})
        mod_trap_key = trapKey[4:]
        possibilities = []
        for (i, key) in enumerate(team_keys):
            # print("Mod Key: " + mod_trap_key, score.get('endGameRobot' + str(i), 'Donut'))
            if score.get('endGameRobot' + str(i+1), 'None') == mod_trap_key:
                possibilities.append(key)

        if len(possibilities) == 0:
            return team_keys

        else:
            return possibilities




        

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

    # def validate_match(self, match:dict) -> bool:
    #     return True

    def predict_alliance(self, color:str, match:dict, teams:dict, prediction:dict):

        auto_points = 0
        teleop_points = 0
        endgame_points = 0

        notes = 0

        teleop_speaker_notes = 0
        teleop_amp_notes = 0

        speaker_during_amp = 0

        basic_climbs = 0
        trap_climbs = 0


        for team_key in match.get('alliances',{}).get(color,{}).get('team_keys',[]):
            team = teams.get(team_key,{})
            auto_points += team.get('autoPoints',0)
            notes += team.get('autoAmpNoteCount',0) + team.get('autoSpeakerNoteCount',0)
            teleop_speaker_notes += team.get('teleopSpeakerNoteCount',0)
            teleop_amp_notes += team.get('teleopAmpNoteCount',0)
            endgame_points += team.get('climb',0) + 5 * team.get('trapNoteCount',0)

            if(team.get('trapNoteCount')) > 0.8:
                trap_climbs +=1
            elif(team.get('climb',0)>2.5):
                basic_climbs +=1
            
            if basic_climbs > 2:
                endgame_points +=2

            if team.get('teleopSpeakerNoteCount',0) > 13:
                speaker_during_amp += 2 
            else:
                speaker_during_amp += 1

        robot_activity = teleop_speaker_notes + teleop_amp_notes
        notes += robot_activity
        while robot_activity > 0:
            if robot_activity > 3:
                robot_activity -=2
                teleop_points +=2

                notes_in_speaker = min(robot_activity, min(speaker_during_amp, 4))
                teleop_points += 5 * notes_in_speaker
                robot_activity -= notes_in_speaker

            else:
                teleop_points += 2 * robot_activity
                robot_activity = 0

            
        score = auto_points + teleop_points + endgame_points

            
        prediction[f"{color}_teams"] = match.get('alliances',{}).get(color,{}).get('team_keys',[])
        prediction[f"{color}_score"] = round(score,2)
        prediction[f"{color}_notes"] = round(notes,2)
        prediction[f"{color}_auto"] = round(auto_points,2)
        prediction[f"{color}_teleop"] = round(teleop_points,2)
        prediction[f"{color}_endgame"] = round(endgame_points,2)
        prediction[f"{color}_climbs"] = round(basic_climbs + trap_climbs,2)



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

        if prediction['blue_endgame'] > 10 and prediction['blue_climbs'] >= 2:
            prediction['blue_harmony_rp'] = 1
        else:
            prediction['blue_harmony_rp'] = 0
        
        if prediction['red_endgame'] > 10 and prediction['red_climbs'] >= 2:
            prediction['red_harmony_rp'] = 1
        else:
            prediction['red_harmony_rp'] = 0

        if prediction['blue_notes'] >= 18:
            prediction['blue_melody_rp'] = 1
        else:
            prediction['blue_melody_rp'] = 0

        if prediction['red_notes'] >= 18:
            prediction['red_melody_rp'] = 1
        else:
            prediction['red_melody_rp'] = 0


        return prediction
    
    def parse_rps(self, match:dict) -> tuple:
        blue_rp = 0
        red_rp = 0
        
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('melodyBonusAchieved'))
        blue_rp += int(match.get('score_breakdown',{}).get('blue',{}).get('ensembleBonusAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('melodyBonusAchieved'))
        red_rp += int(match.get('score_breakdown',{}).get('red',{}).get('ensembleBonusAchieved'))
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
        print(passing)
        return passing
