import redis
import json
import time
import config

redis = redis.Redis(host = config.REDIS_HOST, port = config.REDIS_PORT)

def is_cache_available()->bool:
    try:
        return redis.ping()
    except ConnectionError as e:
        print("Unable to access Redis cache. No connection to cache.", e)
        return False
    except Exception as e:
        print("An unknown error occured when trying to ping the Redis cache.", e)
        return False

def cache_json(key: str, dictionary:dict, etag:str = None, last_modified:float=time.time(), tba:bool=False)->bool:
    try:
        dictionary['metadata'] = {'last_modified':last_modified, 'etag': etag,'tba':tba}
        d = json.dumps(dictionary)
        success = redis.set(key, d)
        return success
    except ConnectionError as e:
        print("Unable to access Redis cache. No connection to cache.", e)
        return False
    except Exception as e:
        print("An unknown error occured when trying to store data in the Redis cache", e)
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
        return False
    except Exception as e:
        print("An unknown error occured when trying to retrieve data from the Redis cache", e)
        return False


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
