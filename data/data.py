import data.tba as tba
import data.datacache as datacache


# Gets the latest data for the supplied key, if the data not available locally try to get it on the blue alliance
def get(key:str, update:bool = True, from_tba=False) -> dict:
    result = datacache.get_json(key)
    if result is None:
        if from_tba:
            tba_data, etag = tba.get(key)
            datacache.cache_json(key, tba_data, etag=etag)
            return tba_data
        else:
            return None
    elif update and result['metadata']['tba']:
        tba_data, etag = tba.get(key, etag=result['metadata']['etag'])
        if tba_data is not None and etag is not None:
            datacache.cache_json(key, tba_data, etag=etag)
            return tba_data
        else:
            return result
    else:
        return result

# Stores the Supplied Dictionary in the Redis Cache
def store(key:str, data:dict) -> bool:
    return cache_json(key, data)


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