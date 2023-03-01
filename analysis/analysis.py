from config import FRC_GAMES
from data.data import get, store, get_year_event_list_tba
from analysis.event import Event
from games.frc_game import FRCGame
from datetime import datetime, timedelta
import traceback






def lookup_game(year: int, event_key:str) -> FRCGame:
    if year in FRC_GAMES:
        return FRC_GAMES[year]
    elif year + "_" + event_key in FRC_GAMES:
        print("Heads up, The desired event is showing up as a possible custom game. This featureset hasn't been tested yet.")
        return FRC_GAMES[year+"_"+event_key]
    else:
        print(f"No valid Ruleset found for Year: {year}. Either Polar Forecast cannot handle this game, or it is disabled.")
        return None



def update_event(tba_event):
    year = tba_event.get('year',2023)
    event_key = tba_event.get('event_code')
    game = lookup_game(year, event_key)
    if game is not None:
        event = Event(tba_event, game)
        event.update()


def get_as_date(date)   :
    return datetime.strptime(date, '%Y-%m-%d')

# Function called by the polling API to perform generic updates on all of the events. 
def update():
    print("Updating Events")
    # update_event(2023, "week0")
    today = datetime.now()
    events = get_year_event_list_tba(2023)
    for event in events:
        try:
            start = get_as_date(event['start_date']) - timedelta(days = 1)
            end = get_as_date(event['end_date']) + timedelta(days = 1)
            #if event['event_code'] in ["hop", "new", "gal", "carv", "roe", "tur"]:
            # if event['event_code'] == 'cokc' or event['event_code'] == 'cocri' or event['event_code'] == 'coden':
            #if today >= start:
            if today >= start and today <= end:
            # if event['event_code'] =='isde1':
                update_event(event)
                
            

        except Exception as e:
            print("Error:", e)
            traceback.print_exc()

    pass



if __name__ == '__main__':
    pass

    
