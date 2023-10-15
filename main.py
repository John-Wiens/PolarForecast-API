
from analysis.analysis import update_event, update
from data.data import get_all_search_keys, get


if __name__ == '__main__':
    print("Running Local Polar Forecast Analysis")
    update_event(2023, "coden")
    #update(force_update = True)
    # get_all_search_keys()

    
