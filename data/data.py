import data.tba as tba
import data.datacache as datacache

# Blue Alliance sources for Data
matches_request_base:str = "/event/{year}{event}/matches"
teams_request_base:str = "/event/{year}{event}/teams"
ranking_request_base:str = "/event/{year}{event}/rankings"
event_list_request_base:str = "/events/{year}/simple"

# Generated Data Locations
team_key_base: str = "/year/{year}/event/{event}/teams/{team}"






# Gets the latest data for the supplied key, if the data not available locally try to get it on the blue alliance
def get(key:str, update:bool = True, from_tba:bool = False) -> dict:
    result = datacache.get_json(key)
    if result is None:
        if from_tba:
            tba_data, etag = tba.get(key)
            datacache.cache_json(key, tba_data, etag=etag)
            return datacache.get_json(key)
        else:
            return None
    elif update and result['metadata']['tba']:
        tba_data, etag = tba.get(key, etag=result['metadata']['etag'])
        if tba_data is not None and etag is not None:
            datacache.cache_json(key, tba_data, etag=etag)
            return datacache.get_json(key)
        else:
            return result
    else:
        return result

def get_from_index(index:str, remove_metadata:bool = True, remove_intermediate:bool = True) -> dict:
    index_data = get(index)
    if index_data is None:
        return 404
    else:
        data = []
        for key in index_data['data']['keys']:
            ret = get(key, update = False)
            if ret is not None:
                cleaned = clean_response(ret, remove_metadata=True, remove_intermediate = remove_intermediate)
                data.append(cleaned)
            
        return {"data":data, "metadata": index_data['metadata']}


# Stores the Supplied Dictionary in the Redis Cache
def store(key:str, data:dict, index = False) -> bool:
    return datacache.cache_json(key, data, index = index)


# Removes metadata and solver data from response
def clean_response(data:dict, remove_metadata:bool = True, remove_intermediate:bool = True) -> dict:
    if remove_metadata and 'metadata' in data:
        del data['metadata']
    if remove_intermediate:
        remove_keys = []
        for key in data.keys():
            if key[0] == "_":
                remove_keys.append(key)
        for key in remove_keys:
            del data[key]
    return data

# Blue Alliance Match Data
def get_year_event_matches_tba(year:int, event:str):
    key = matches_request_base.format(year=year, event=event)
    return get(key, update = True, from_tba=True).get('data',{})

def store_year_event_matches_tba(year:int, event:str, data:dict):
    key = matches_request_base.format(year=year, event=event)
    return store(key, data, index = False)


# Blue Alliance Team Data
def get_year_event_teams_tba(year:int, event:str):
    key = teams_request_base.format(year=year, event=event)
    return get(key, update = True, from_tba=True).get('data',{})

def store_year_event_teams_tba(year:int, event:str, data:dict):
    key = teams_request_base.format(year=year, event=event)
    return store(key, data, index = False)


# Blue Alliance Ranking Data
def get_year_event_rankings_tba(year:int, event:str):
    key = ranking_request_base.format(year=year, event=event)
    return get(key, update = True, from_tba=True).get('data',{})

def store_year_event_rankings_tba(year:int, event:str, data:dict):
    key = ranking_request_base.format(year=year, event=event)
    return store(key, data, index = False)


# Blue Alliance Event Data
def get_year_event_list_tba(year:int):
    key = event_list_request_base.format(year = year)
    return get(key, from_tba = True).get('data',{})

def store_year_event_list_tba(year:int, data:dict):
    key = event_list_request_base.format(year = year)
    return store(key, data, index = False)


# Team Event Performance Data
def get_year_event_team(year:int, event:str, team:str):
    key = team_key_base.format(year=year, event=event, team=team)
    return get(key)

def store_year_event_team(year:int, event:str, team:str, data:dict):
    key = team_key_base.format(year=year, event=event, team=team)
    return store(key, data, index = True)

def get_year_event_team_index(year:int, event:str, remove_metadata = True, remove_intermediate = True):
    key = datacache.get_index_key(team_key_base.format(year=year, event=event, team=""))
    return get_from_index(key, remove_metadata = remove_metadata, remove_intermediate = remove_intermediate)






if __name__ == '__main__':
    print("Performing Data Access Test")
    data = get("/event/2022code/matches")
    if data is not None:
        print("Successfully got data")
    else:
        print("Data Retrieval Failed")

    data = get("/event/2022code/matches",update = True)
    if data is not None:
        print("Successfully got data from TBA (Forced)")
    else:
        print("Data Retrieval Failed")

    data = get("/event/2022code/matches",update = True)
    if data is not None:
        print("Successfully got data from Cache")
    else:
        print("Data Retrieval Failed")