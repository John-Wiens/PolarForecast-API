# PolarForecast-API
This is a repository to store the API and data analysis components of the Polar Forecast FRC Scouting System.

The Polar Forecast is designed to automatically compute and provide teams information about first events based on data from the FIRST FRC API here[https://frc-events.firstinspires.org/services/API]. Pursuant to the terms of use of the FIRST API, any application using data provided by the PolarForecast API should provide all data attribution back to FIRST as documented here [https://frc-events.firstinspires.org/services/API/terms].

## Setup development environment

The polar forecast development environment uses a local redis image to work with data. The redis image can be setup easily with docker using the command below.
```
docker run -p 6379:6379 --name pf-redis redis redis-server --save 60 1 --loglevel warning
```

## Environment variables
The following environment variables are used by the Polar Forecast API for configuring the user environment.
PF_

