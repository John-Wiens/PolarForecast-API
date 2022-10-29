import numpy as np



def smart_solve(matches, teams, stats):
    team_array, score_array = build_score_matrix(matches, teams, stats)

    

    pass


def linear_solve(matches, teams, stats):
    team_array, score_array = build_score_matrix(matches, teams, stats)
    print(team_array, score_array)
    pass


def nnls_solve(matches, teams, stats):

    pass

def linked_solve(matches, teams, stats):

    pass


def build_score_matrix(matches, teams, stats):
    num_teams = len(teams)
    num_matches = len(matches)
    num_stats = len(stats)

    team_array = np.zeros([num_matches*2, num_teams])
    score_array = np.zeros([num_matches*2, num_stats])

    i = 0
    for match in matches:
        metric_count = 0
        for stat in stats:
            score_array[i][metric_count] = match["blue_" + metric]
            score_array[num_matches + i][metric_count] = match["red_" + metric]
            metric_count +=1
        
        for j in range(0,3):
            blue_index = teams["frc"+match["blue"+str(j)]]['index']
            red_index = teams["frc"+match["red"+str(j)]]['index']
            team_array[i][blue_index] = 1
            team_array[num_matches+i][red_index] = 1
            
        i+=1

    return team_array, score_array