import redis
import json
import time
import config

redis = redis.Redis(host = config.REDIS_HOST, port = config.REDIS_PORT)

def get_index_key(key:str):
    return key[:key.rindex("/")] + "/index"

def is_cache_available()->bool:
    try:
        return redis.ping()
    except ConnectionError as e:
        print("Unable to access Redis cache. No connection to cache.", e)
        return False
    except Exception as e:
        print("An unknown error occured when trying to ping the Redis cache.", e)
        return False

def get_json(key:str)->dict:
    try:
        data = redis.get(key)
        if data is not None:
            return json.loads(data)
        else:
            return None
    except ConnectionError as e:
        print("Unable to access Redis cache. No connection to cache.", e)
        return None
    except Exception as e:
        print("An unknown error occured when trying to retrieve data from the Redis cache", e)
        return None

def cache_json(key: str, dictionary:dict, etag:str = None, last_modified:float=time.time(), tba:bool=False, index=False)->bool:
    try:
        dictionary['metadata'] = {'last_modified':last_modified, 'etag': etag,'tba':tba}
        d = json.dumps(dictionary)
        success = redis.set(key, d)
        if index and success:
            sub_key = get_index_key(key)
            index_record = get_json(sub_key)
            if index_record is not None:
                if key not in index_record['data']['keys']:
                    index_record['data']['keys'].append(key)
                else:
                    index_record['data']['keys'] = [key]
                cache_json(sub_key, index_record, index = False)
            else:
                print("Creating new Index: ", sub_key)
                index_record = {
                    "data":{
                        "keys":[sub_key]
                    }
                }
                cache_json(sub_key, index_record, index = False)
        
        return success
    except ConnectionError as e:
        print("Unable to access Redis cache. No connection to cache.", e)
        return False
    except Exception as e:
        print("An unknown error occured when trying to store data in the Redis cache", e)
        print(f"Issue Caused while storing key: {key}, Data: {dictionary}")
        return False


def get_keys(index: str)->list:
    return redis.scan_iter(f"{index}/*")

def get_data_with_key(key:str) -> dict:
    keys = get_keys(key)
    data = redis.mget(keys)
    response = []
    for row in data:
        row_json = json.loads(row)
        del row_json['metadata']
        response.append(row_json)
    return {"data": response}


if __name__ == '__main__':
    print('Performing Redis Test')
    if is_cache_available():
        print('Setting Key in Redis')
        print(cache_json('test-key', {"redis_test": True}))
        print('Reading Key from Redis')
        value = get_json('test-key')
        print(value)
        print('Complete.')
    else:
        print("Unable to Reach Cache")
