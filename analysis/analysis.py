from config import FRC_GAMES
from data.data import get, store
from analysis.event import Event
from games.frc_game import FRCGame








# Function called by the polling API to perform generic updates on all of the events. 
def update():
    pass


def lookup_game(year: int, event_key:str) -> FRCGame:
    if year in FRC_GAMES:
        return FRC_GAMES[year]
    elif year + "_" + event_key in FRC_GAMES:
        print("Heads up, The desired event is showing up as a possible custom game. This featureset hasn't been tested yet.")
        return FRC_GAMES[year+"_"+event_key]
    else:
        print(f"No valid Ruleset found for Year: {year}. Either Polar Forecast cannot handle this game, or it is disabled.")
        return None



def update_event(year, event_key):
    game = lookup_game(year, event_key)
    if game is not None:
        event = Event(year, event_key, game)
        event.update()


if __name__ == '__main__':
    pass

    