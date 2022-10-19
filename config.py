import os

REDIS_HOST = os.environ.get("PF_REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("PF_REDIS_PORT", 6379)
TBA_API_KEY = os.environ.get("PF_TBA_API_KEY", "")
TBA_POLLING = os.environ.get("PF_TBA_POLLING", True)


if TBA_API_KEY == "":
    print("No API KEY for Blue alliance specified.")
