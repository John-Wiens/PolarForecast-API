from config import FRC_GAMES
from data.data import get, store
from analysis.event import Event








# Function called by the polling API to perform generic updates on all of the events. 
def update():
    pass




def update_event(year, event_key):
    if year in FRC_GAMES:
        event = Event(year, event_key, FRC_GAMES[year])
        event.update()
    else:
        print(f"No valid Ruleset found for Year: {year}. Either Polar Forecast cannot handle this game, or it is disabled.")



if __name__ == '__main__':
    pass

    