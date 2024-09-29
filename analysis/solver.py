import numpy as np

from scipy.optimize import nnls

SMART_SOLVER = 'smart_solve'
LINKED_SOLVER = 'linked'
SUM_SOLVER = 'sum'
CUSTOM_SOLVER = 'custom'
POST_SOLVER = 'post'

def smart_solve(matches, teams, stats):
    team_array, score_array = build_score_matrix(matches, teams, stats)

    num_equations = 2 * len(matches) + len(team_array)
    num_variables = min(len(teams), 6 * len(matches))

    # Solve Entry cases with OPR
    if num_equations < num_variables:
        hist_team_array, hist_score_array = build_historical_matrix(teams, stats)
        team_array = np.concatenate((team_array, hist_team_array), axis = 0)
        score_array = np.concatenate((score_array, hist_score_array), axis = 0)
        solution = np.linalg.lstsq(team_array,score_array,rcond=None)[0]
        return parse_solution(solution, teams, stats)
    
    else: 
        if num_equations < 2 * len(teams):
            hist_team_array, hist_score_array = build_historical_matrix(teams, stats)
            team_array = np.concatenate((team_array, hist_team_array), axis = 0)
            score_array = np.concatenate((score_array, hist_score_array), axis = 0)

        X = np.zeros([team_array.shape[1],score_array.shape[1]])
        
        for i in range(0,score_array.shape[1]):
            if(len(score_array[:,i]) > 0):
                X[:,i] = nnls(team_array,score_array[:,i])[0]
        return parse_solution(X, teams, stats)
    


    # num_equations = 2 * len(matches) # Each match produces 2 equations (red and blue)
    # num_variables = min(len(teams), 6 * len(matches)) # Each match loads 6 new teams into the system, until all teams have played. 
    
    # if num_equations > num_variables:
    #     return nnls_solve(matches, teams, stats)
    # else:
    #     return linear_solve(matches, teams, stats)

def linear_solve(matches, teams, stats):
    team_array, score_array = build_score_matrix(matches, teams, stats)
    solution = np.linalg.lstsq(team_array,score_array,rcond=None)[0]
    return parse_solution(solution, teams, stats)


def nnls_solve(matches, teams, stats):
    team_array, score_array = build_score_matrix(matches, teams, stats)
    X = np.zeros([team_array.shape[1],score_array.shape[1]])
    for i in range(0,score_array.shape[1]):
        if(len(score_array[:,i]) > 0):
            X[:,i] = nnls(team_array,score_array[:,i])[0]
    return parse_solution(X, teams, stats)

def parse_solution(solution, teams, stats):
    for team in teams.values():
        for index, stat in enumerate(stats):
            team[stat] = solution[team['_index']][index]
    return teams

def linked_solve(matches, teams, stats):
    for stat in stats:
        list_name = "_"+stat.stat_key+"_list"
        for match in matches:
            for i in range(0, 3):
                blue_key = match['alliances']['blue']['team_keys'][i]
                red_key = match['alliances']['red']['team_keys'][i]

                blue_value = stat.mapper.get(match['score_breakdown']['blue'][stat.linked_key+str(i+1)],0)
                red_value = stat.mapper.get(match['score_breakdown']['red'][stat.linked_key+str(i+1)],0)

                if list_name in teams[blue_key]:
                    teams[blue_key][list_name].append(blue_value)
                else:
                    teams[blue_key][list_name] = [blue_value]
                if list_name in teams[red_key]:
                    teams[red_key][list_name].append(red_value)
                else:
                    teams[red_key][list_name] = [red_value]

        for team in teams.values():
            if len(team.get(list_name,[])) > 0:
                team[stat.stat_key] = sum(team[list_name]) / len(team[list_name])
            else:
                team[stat.stat_key] = 0
    return teams

def sum_solve(teams, stat):
    for team in teams.values():
        total = 0
        for key, weight in zip(stat.component_stats, stat.weights):
            total += team[key] * weight

        team[stat.stat_key] = total

    return teams

def build_score_matrix(matches, teams, stats):
    num_teams = len(teams)
    num_matches = len(matches)
    num_stats = len(stats)

    print(num_matches)

    team_array = np.zeros([num_matches*2, num_teams])
    score_array = np.zeros([num_matches*2, num_stats])

    i = 0
    for match in matches:
        for stat_count, stat in enumerate(stats):
            print(match)
            score_array[i][stat_count] = match.get("score_breakdown",{}).get("blue",{}).get(stat,0)
            score_array[num_matches + i][stat_count] = match.get("score_breakdown",{}).get("red",{}).get(stat,0)
            stat_count +=1
        
        for j in range(0,3):
            blue_index = teams[match['alliances']['blue']['team_keys'][j]]['_index']
            red_index = teams[match['alliances']['red']['team_keys'][j]]['_index']
            team_array[i][blue_index] = 1
            team_array[num_matches+i][red_index] = 1
            
        i+=1

    print(team_array)    

    return team_array, score_array

def build_historical_matrix(teams, stats):
    extra_equations = 0
    for team in teams:
        if teams.get(team,{}).get('historical',False):
            extra_equations +=1
    
    team_array = np.zeros([extra_equations, len(teams)])
    score_array = np.zeros([extra_equations, len(stats)])

    i = 0
    for team in teams:
        if teams.get(team,{}).get('historical',False):
            team_array[i][teams.get(team,{}).get('_index',0)] = 1
            for stat_count, stat in enumerate(stats):
                score_array[i][stat_count] = teams.get(team,{}).get(stat,0)
            i+=1
    return team_array, score_array
