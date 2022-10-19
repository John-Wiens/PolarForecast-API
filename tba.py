import requests
import json
import config

#
# This file contains helper functions that make it easier to manage blue alliance function calls. 
# All calls to information in the blue alliance should use the support methods located here. 
#

API_URL = 'https://www.thebluealliance.com/api/v3'
AUTH_KEY = config.TBA_API_KEY

# Returns whether the system has access to the Blue Alliance
def check_connection() -> bool:
    try:
        get('/status')
        return True
    except Exception as e:
        print(e)
        return False

# Returns a dict with the value of the returned data, followed by the key to be used when making the next transaction
def get(endpoint:str, etag:str="") -> tuple:
    try:
        if etag != None:
            header = {'X-TBA-Auth-Key':AUTH_KEY,'If-None-Match':etag}
        else:
            header = {'X-TBA-Auth-Key':AUTH_KEY}
        response = requests.get(API_URL+endpoint, headers=header)

        if response.status_code == 200:
            return {'data': response.json()}, response.headers['ETag']
        elif response.status_code == 304:
            return None, response.headers['ETag']
        else:
            print("The Blue Alliance API responded with Unexpected Error Code:", response.status_code, response.text)
    except Exception as e:
        print("An Unknown Exception has occured when pulling data from TBA", e)



if __name__ == '__main__':
    print('Performing TBA Test')
    if check_connection():
        print('TBA Connection Successful')
        data, tag = get('/event/2022code/matches')
        if data != None:
            print("TBA Query Successful")
        else:
            print("TBA Query Failed")
        data, tag = get('/event/2022code/matches', etag = tag)
        if data == None and tag != None:
            print("TBA Cache Returned 304 as expected")
        else:
            print("Failure In Cache Test for TBA")
    else:
        print("Unable to Reach TBA")

