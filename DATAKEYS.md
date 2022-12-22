

# Data Indecies and Keying
The below document serves as a common record for the keying scheme used to access all of the data in Polar Forecast. It should help to reduce accidently re-using keys and ensures that future users don't need to survey the codebase to find what key is needed to store a given piece of information. Note, These will not be equal to their corresponding rest endpoints since this also encodes blue alliance data source locations.

### /year/{year}/event/{event}/team/{team}
Team performance data for a given year and team.

### /year/{year}/event/{event}/team/index
Auto Generated Data Index including the stats for each team.

### /event/{year}{event}/matches
Blue alliance match data for a given year and event.

### /event/{year}{event}/teams
Blue alliance team data for a given year and event.

### /event/{year}{event}/rankings
Blue alliance team data for a given year and event.
