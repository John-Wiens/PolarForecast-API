import os
from games.rapid_react_2022 import RapidReact2022


# Specify Deployment Parameters
REDIS_HOST = os.environ.get("PF_REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("PF_REDIS_PORT", 6379)
REDIS_PRIMARY_KEY = os.environ.get("PF_REDIS_PRIMARY_KEY", "")

REDIS_STRICT = os.environ.get("PF_REDIS_STRICT", True)

TBA_API_KEY = os.environ.get("PF_TBA_API_KEY", "")


if TBA_API_KEY == "":
    print("No API KEY for Blue alliance specified.")


# Specify Feature Flags 
TBA_POLLING = os.environ.get("PF_TBA_POLLING", True) # Specifies if the Polar Forecast API should Poll Blue Alliance for Data.
TBA_POLLING_INTERVAL = os.environ.get("PF_TBA_POLLING_INTERVAL", 10*60) # Polling invterval in seconds. 


MATCH_SANITIZATION = os.environ.get('PF_MATCH_SANITIZATION', True) # Specifies if the Polar Forecast API should skip matches that fail data integrity checks. 




# Specify which games are enabled for this analysis system
FRC_GAMES = {
    2022: RapidReact2022
}
