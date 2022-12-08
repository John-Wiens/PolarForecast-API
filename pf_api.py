import analysis.analysis

from config import TBA_POLLING, TBA_POLLING_INTERVAL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from data.data import get, clean_response, get_from_index
from analysis.analysis import lookup_game

app = FastAPI()

run_analysis = True

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
    key = f"/{year}/{event}/{team}"
    data = get(key, update = False, from_tba=False)
    if data is None:
        raise HTTPException(status_code=404, detail="Could not find the supplied key in the database.")
    response = clean_response(data, remove_metadata = not include_metadata, remove_intermediate = not include_intermediate)
    return response

@app.get("/{year}/{event}/stats")
def read_item(year:int, event:str, include_metadata:bool = False, include_intermediate:bool = False ):
    key = f"/{year}/{event}"
    response = get_from_index(key, remove_metadata = not include_metadata, remove_intermediate = not include_intermediate)
    if response is None:
        raise HTTPException(status_code=404, detail="Could not find the supplied key in the database.")
    return response

@app.get("/{year}/{event}/stat_description")
def read_item(year:int, event:str):
    game_model = lookup_game(year, event)
    if game_model is None:
        raise HTTPException(status_code=404, detail="Could not a game matching the supplied parameters")
    game = game_model()
    data = []
    
    for stat in game.stats:
        data.append(stat.get_stat_description())
        
    return {"data": data}

@app.on_event("startup")
@repeat_every(seconds=TBA_POLLING_INTERVAL)
def update_database():
    if TBA_POLLING:
        analysis.update()


