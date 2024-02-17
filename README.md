# PolarForecast-API
This is a repository to store the API and data analysis components of the Polar Forecast FRC Scouting System.

The Polar Forecast API is Powered by The Blue Alliance. For more FRC related data, check out thebluealliance.com

## Setup development environment

The polar forecast development environment uses a local redis image to work with data. The redis image can be setup easily with docker using the command below.
```
docker run -p 6379:6379 --name pf-redis redis redis-server --save 60 1 --loglevel warning
```

## Environment variables
The following environment variables are used by the Polar Forecast API for configuring the user environment.
`PF_REDIS_HOST` - Specifies the Host IP of the redis database. Defaults to localhost
`PF_REDIS_PORT` - Specifies the Port of the redis database. Defaults to 6379
`PF_TBA_API_KEY` - Specifies the API key to be used with the blue alliance API. There is no default value for this variable. If not specified, the Polar Forecast API will be limited to cached data only.


## Caching Setup

The Polar Forecast uses REDIS for caching data as it is acquired. The redis cache is used for both raw blue alliance data, as well as processed data created by polar forecast. All data loaded into the cache is stored as string encoded json data. When data is loaded into the cache, metadata is added to the data record itself for future utility. The metadata currently follows the following format.

```
{
    "tba":bool -> True if the data is directly cached from the blue alliance.
    "last_modified":float -> unixtime of when the data was stored
    "etag": str -> The etag given to the data the last time it was retrieved from the blue alliance.
}
```

To Simplify data storage all data access should be done using the get and store methods from data.py. These methods will automatically handle etags and caching to simplify things for a user accessing the cache. For blue alliance entries users can forcibly update the entry by passing the update parameter to the cache.


## Running the Application
The PolarForecastAPI can be run using the following command

python3 -m uvicorn pf_api:app --host 0.0.0.0 --port 8000