import random

def get_random_team(team_list:list, exclude_teams:list = []):
    index = int(random.random() * len(team_list))
    team = team_list[index]
    while team in exclude_teams:
        index = int(random.random() * len(team_list))
        team = team_list[index]

    return team

def get_random_alliances(team_list:list, exclude_teams:list = []):
    blue1 = get_random_team(team_list, exclude_teams = exclude_teams)
    blue2 = get_random_team(team_list, exclude_teams= exclude_teams + [blue1])
    blue3 = get_random_team(team_list, exclude_teams= exclude_teams + [blue1, blue2])
    red1 = get_random_team(team_list, exclude_teams= exclude_teams + [blue1, blue2, blue3])
    red2 = get_random_team(team_list, exclude_teams= exclude_teams + [blue1, blue2, blue3, red1])
    red3 = get_random_team(team_list, exclude_teams= exclude_teams + [blue1, blue2, blue3, red1, red2])
    return [blue1, blue2, blue3], [red1, red2, red3]


def get_random_schedule(teams:dict, schedule_length:int):
    team_list = list(teams.keys())
    exclude_teams = []
    matches = []
    for j in range(0, schedule_length):
        if len(team_list) - len(exclude_teams) < 6:
            exclude_teams = []
        blue_alliance, red_alliance = get_random_alliances(team_list, exclude_teams = exclude_teams)
        exclude_teams += blue_alliance
        exclude_teams += red_alliance


        matches.append({
            'alliances':{'red': {'team_keys': red_alliance}, 'blue': {'team_keys': blue_alliance}}
        })

    return matches


def simulate_event(matches:list, teams:dict, prediction_function, rp_function):
    rps = {}

    for team in teams.keys():
        rps[team] = 0

    blue_keys = []
    red_keys = []
    for match in matches:
        result_time = match.get("post_result_time",-1)
        blue_rp = 0
        red_rp = 0
        if result_time is not None and result_time > 0:
            if match.get('comp_level','') == 'qm':
                blue_rp, red_rp = rp_function(match)

        else:
            prediction = prediction_function(match, teams)
            if len(red_keys) == 0:
                for key in prediction.keys():
                    if '_rp' in key:
                        if 'red' in key:
                            red_keys.append(key)
                        elif 'blue' in key:
                            blue_keys.append(key)
            
            for key in blue_keys:
                blue_rp += prediction[key]

            for key in red_keys:
                red_rp += prediction[key]
            
        for team in match.get('alliances',{}).get('blue',{}).get('team_keys',[]):
            rps[team] += blue_rp
        
        for team in match.get('alliances',{}).get('red',{}).get('team_keys',[]):
            rps[team] += red_rp


    return rps
            

