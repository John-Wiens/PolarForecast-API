import numpy as np

from scipy.optimize import nnls

def smart_solve(matches, teams, stats):
    num_equations = 2 * len(matches) # Each match produces 2 equations (red and blue)
    num_variables = min(len(teams), 6 * len(matches)) # Each match loads 6 new teams into the system, until all teams have played. 
    
    if num_equations > num_variables:
        return nnls_solve(matches, teams, stats)
    else:
        return linear_solve(matches, teams, stats)

def linear_solve(matches, teams, stats):
    team_array, score_array = build_score_matrix(matches, teams, stats)
    solution = np.linalg.lstsq(team_array,score_array,rcond=None)[0]
    return parse_solution(solution, teams, stats)


def nnls_solve(matches, teams, stats):
    team_array, score_array = build_score_matrix(matches, teams, stats)
    X = np.zeros([team_array.shape[1],score_array.shape[1]])
    for i in range(0,score_array.shape[1]):
        X[:,i] = nnls(team_array,score_array[:,i])[0]
    return parse_solution(X, teams, stats)

def parse_solution(solution, teams, stats):
    for team in teams.values():
        for index, stat in enumerate(stats):
            team[stat] = solution[team['index']][index]
    return teams

def linked_solve(matches, teams, stats):
    for match in matches:
        for stat in stats:
            for i in range(0,3):
                pass
    pass


def build_score_matrix(matches, teams, stats):
    num_teams = len(teams)
    num_matches = len(matches)
    num_stats = len(stats)

    team_array = np.zeros([num_matches*2, num_teams])
    score_array = np.zeros([num_matches*2, num_stats])

    i = 0
    for match in matches:
        for stat_count, stat in enumerate(stats):
            score_array[i][stat_count] = match["score_breakdown"]["blue"][stat]
            score_array[num_matches + i][stat_count] = match["score_breakdown"]["red"][stat]
            stat_count +=1
        
        for j in range(0,3):
            blue_index = teams[match['alliances']['blue']['team_keys'][j]]['index']
            red_index = teams[match['alliances']['red']['team_keys'][j]]['index']
            team_array[i][blue_index] = 1
            team_array[num_matches+i][red_index] = 1
            
        i+=1

    return team_array, score_array