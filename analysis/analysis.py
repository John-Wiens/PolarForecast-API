from config import FRC_GAMES, ENABLE_BACKPOP
from data.data import get, store, get_year_event_list_tba, get_all_search_keys, update_search_key_cache, get_year_event_team_index, store_year_team_ranks
from analysis.event import Event
from games.frc_game import FRCGame
from datetime import datetime, timedelta
import traceback






def lookup_game(year: int, event_key:str) -> FRCGame:
    if year in FRC_GAMES:
        return FRC_GAMES[year]
    elif str(year) + "_" + event_key in FRC_GAMES:
        print("Heads up, The desired event is showing up as a possible custom game. This featureset hasn't been tested yet.")
        return FRC_GAMES[year+"_"+event_key]
    else:
        print(f"No valid Ruleset found for Year: {year}. Either Polar Forecast cannot handle this game, or it is disabled.")
        return None



def update_event(tba_event):
    year = tba_event.get('year', 2024)
    event_key = tba_event.get('event_code')
    game = lookup_game(year, event_key)
    if game is not None:
        event = Event(tba_event, game)
        event.update()


def get_as_date(date):
    return datetime.strptime(date, '%Y-%m-%d')

# Function called by the polling API to perform generic updates on all of the events. 
def update(force_update = False):
    print("Updating Events")
    # update_event(2023, "week0")
    today = datetime.now()
    events = get_year_event_list_tba(2024)
    events = sorted(events, key=lambda d: get_as_date(d['end_date']))
    keys = [elem.get('key','missing') for elem in get_all_search_keys()['data']]
    for event in events:
        try:
            start = get_as_date(event['start_date']) - timedelta(days = 1)
            end = get_as_date(event['end_date']) + timedelta(days = 1)

            # Fix Missing Data
            #if force_update or ENABLE_BACKPOP and end < today and not event['key'] in keys:
            #     print("Updating Missing Data", event['key'])
            #     update_event(event)


            # if event['event_code'] in ["hop", "new", "gal", "joh", "arc", "cur","dal","mil","cmptx"]:

            # if event['event_code'] == 'cokc' or event['event_code'] == 'cocri' or event['event_code'] == 'coden':
            #if today >= start:
            # if today >= start and today <= end:
            # if event['event_type'] == 2:
            if event['event_code'] =='week0':
               update_event(event)
                
            

        except Exception as e:
            print("Error:", e)
            traceback.print_exc()
    update_search_key_cache()
    pass

def update_global():
    today = datetime.now()
    events = get_year_event_list_tba(2024)
    events = sorted(events, key=lambda d: get_as_date(d['end_date']), reverse = False)
    keys = [elem.get('key','missing') for elem in get_all_search_keys()['data']]
    teams = {}
    for event in events:
        if get_as_date(event.get('end_date')) <  today:
            new_teams = get_year_event_team_index(2024, event.get('event_code'))
            
                
            if new_teams is not None:
                team_list = new_teams.get('data')
                for team in team_list:
                    if team.get('_valid_import', True):
                        teams[team.get('key')] = team
    teams = sorted(teams.items(), key=lambda x: x[1].get('OPR',0), reverse = True)

    teams = teams[0:100]
    team_list = []
    for i, team in enumerate(teams):
        team[1]['global_ranking'] = i+1
        team[1].pop('rank',None)
        team[1].pop('historical',None)
        team[1].pop('simulatedRanking',None)
        team[1].pop('expectedRanking',None)
        team[1].pop('schedule',None)
        team_list.append(team[1])
        # print(i+1, team[0], round(team[1].get('OPR',0),2)) 

        # if i > 100:
        #     break
    ranks = {'data': team_list}
    store_year_team_ranks(2023, ranks)

if __name__ == '__main__':
    pass

    
