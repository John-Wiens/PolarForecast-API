
from analysis.analysis import update_event, update, lookup_game
from data.data import get_all_search_keys, get


if __name__ == '__main__':
    print("Running Local Polar Forecast Analysis")
    # update_event("week0")
    update(force_update = False)
    # get_all_search_keys()

    
