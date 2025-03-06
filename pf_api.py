import analysis.analysis
import data.data as source

from config import TBA_POLLING, TBA_POLLING_INTERVAL, FORCE_BACKPOP_ONCE
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every


from analysis.analysis import lookup_game, update, update_global

app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:3000",
    "https://polarforecastfrc.com",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Polar": "Forecast"}


@app.get("/{year}/{event}/{team}/stats")
def read_item(year:int, event:str, team: str, include_metadata:bool = False, include_intermediate:bool = False):
    data = source.get_year_event_team(year, event, team)
    if data is None:
        raise HTTPException(status_code=404, detail="Could not find the supplied key in the database.")
    response = source.clean_response(data, remove_metadata = not include_metadata, remove_intermediate = not include_intermediate)
    return response

@app.get("/{year}/leaderboard")
def read_item(year:int, include_metadata:bool = False, include_intermediate:bool = False):
    data = source.get_year_team_ranks(year)
    if data is None:
        raise HTTPException(status_code=404, detail="Could not find the supplied key in the database.")
    response = source.clean_response(data, remove_metadata = not include_metadata, remove_intermediate = not include_intermediate)
    return response

@app.get("/{year}/{event}/{team}/matches")
def read_item(year:int, event:str, team:str):
    matches = source.get_year_event_team_matches(year, event, team)
    if matches is None:
        raise HTTPException(status_code=404, detail="Could not find any matches.")
    return {'data': matches}

@app.get("/{year}/{event}/{team}/predictions")
def read_item(year:int, event:str, team:str, include_metadata: bool = False, include_intermediate:bool = False):
    matches = source.get_year_event_team_matches(year, event, team)
    predictions = source.get_match_prediction_index(year, event, remove_metadata = not include_metadata, remove_intermediate = not include_intermediate)
    if matches is None:
        raise HTTPException(status_code=404, detail="Could not find any matches.")
    if predictions is None:
        raise HTTPException(status_code=404, detail="Could not find any predictions.")
    
    results = []
    for match in matches:
        for prediction in predictions['data']:
            if match.get('key','') == prediction.get('key','_'):
                results.append(prediction)
    return {'data': results}
        
    if response is None:
        raise HTTPException(status_code=404, detail="Could not find the supplied key in the database.")
    return response

@app.get("/{year}/{event}/{match_key}/match_details")
def read_item(year:int, event:str, match_key:str, include_metadata: bool = False, include_intermediate:bool = False):
    matches = source.get_year_event_matches_tba(year, event)
    match = None
    for m in matches:
        if m.get('key','') == match_key:
            match = m
    if match is None:
        raise HTTPException(status_code=404, detail="Could not find the supplied Match in the database.")
    
    prediction = source.get_match_prediction(year, event, match_key)
    response = {
        'match': match,
        'prediction': prediction,
        'red_teams':[],
        'blue_teams':[]
    }

    for color in ['red', 'blue']:
        for team in match.get('alliances',{}).get(color,{}).get('team_keys',[]):
            team_stats = source.get_year_event_team(year, event, team)
            response[f'{color}_teams'].append(team_stats)

    return response

@app.get("/{year}/{event}/stats")
def read_item(year:int, event:str, include_metadata:bool = False, include_intermediate:bool = False ):
    response = source.get_year_event_team_index(year, event, remove_metadata = not include_metadata, remove_intermediate = not include_intermediate)
    if response is None:
        raise HTTPException(status_code=404, detail="Could not find the supplied key in the database.")
    return response

@app.get("/{year}/{event}/predictions")
def read_item(year:int, event:str, include_metadata:bool = False, include_intermediate:bool = False ):
    response = source.get_match_prediction_index(year, event, remove_metadata = not include_metadata, remove_intermediate = not include_intermediate)
    if response is None:
        raise HTTPException(status_code=404, detail="Could not find the supplied key in the database.")
    return response


@app.get("/{year}/{event}/stat_description")
def read_item(year:int, event:str):
    game_model = lookup_game(year, event)
    if game_model is None:
        raise HTTPException(status_code=404, detail="Could not find a game matching the supplied parameters")
    game = game_model()
    data = []
    
    for stat in game.stats:
        data.append(stat.get_stat_description())

    return {"data": data, "charts": game.charts}

@app.get("/events/{year}")
def read_item(year:int):
    response = source.get_year_event_list_tba(year)
    if response is None:
        raise HTTPException(status_code=404, detail="Could not find the supplied key in the database.")
    return response

@app.get("/search_keys")
def read_item():
    response = source.get_search_key_from_cache()
    if response is None:
        raise HTTPException(status_code=404, detail="Could not find the desired key in the database")
    return response

# @app.get("/{year}/{event}/tba_matches")
# def read_item(year:int, event:str, include_metadata:bool = False):
#     data = source.get_year_event_matches_tba(year, event)
#     if data is None:
#         raise HTTPException(status_code=404, detail="Could not find the supplied key in the database.")
#     response = source.clean_response(data, remove_metadata = not include_metadata, remove_intermediate = False)
#     return response
@app.on_event("startup")
def update_once():
    if FORCE_BACKPOP_ONCE:
        update(force_update=True)


@app.on_event("startup")
@repeat_every(seconds=TBA_POLLING_INTERVAL)
def update_database():
    if TBA_POLLING:
        update()
        


@app.on_event("startup")
@repeat_every(seconds=TBA_POLLING_INTERVAL*6)
def update_leaderboard():
    if TBA_POLLING:
        update_global()





