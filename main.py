
from analysis.analysis import update_event
from data.data import get_all_search_keys


if __name__ == '__main__':
    print("Running Local Polar Forecast Analysis")
    update_event(2022, "code")
    get_all_search_keys()