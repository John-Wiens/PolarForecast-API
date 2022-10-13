import os

REDIS_HOST = os.environ.get("PF_REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("PF_REDIS_PORT", 6379)
FIRST_API_KEY = os.environ.get("PF_FIRST_API_KEY","")
FIRST_API_USERNAME = os.environ.get("PF_FIRST_API_USERNAME","")
