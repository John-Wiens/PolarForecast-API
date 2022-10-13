import redis
import config
import json

redis = redis.Redis(host = config.REDIS_HOST, port = config.REDIS_PORT)


def is_cache_available():
    return redis.ping()

def cache_json(key: str, dictionary:dict):
    d = json.dumps(dictionary)
    success = redis.set(key, d)
    return success

def get_json(key):
    data = redis.get(key)
    if data is not None:
        return json.loads(data)
    else:
        return None


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



