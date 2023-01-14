import analysis.analysis
import data.data as source

from config import TBA_POLLING, TBA_POLLING_INTERVAL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every


from analysis.analysis import lookup_game

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
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

@app.get("/{year}/{event}/stats")
def read_item(year:int, event:str, include_metadata:bool = False, include_intermediate:bool = False ):
    response = source.get_year_event_team_index(year, event, remove_metadata = not include_metadata, remove_intermediate = not include_intermediate)
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
    return {"data": data}


@app.get("/events/{year}")
def read_item(year:int):
    response = source.get_year_event_list_tba(year)
    if response is None:
        raise HTTPException(status_code=404, detail="Could not find the supplied key in the database.")
    return response

# @app.get("/{year}/{event}/tba_matches")
# def read_item(year:int, event:str, include_metadata:bool = False):
#     data = source.get_year_event_matches_tba(year, event)
#     if data is None:
#         raise HTTPException(status_code=404, detail="Could not find the supplied key in the database.")
#     response = source.clean_response(data, remove_metadata = not include_metadata, remove_intermediate = False)
#     return response

@app.on_event("startup")
@repeat_every(seconds=TBA_POLLING_INTERVAL)
def update_database():
    if TBA_POLLING:
        analysis.update()


