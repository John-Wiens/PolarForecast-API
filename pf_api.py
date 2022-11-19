import analysis.analysis

from config import TBA_POLLING, TBA_POLLING_INTERVAL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from data.data import get, clean_response, get_from_index

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


@app.get("/{year}/{event}/{team}")
def read_item(year:int, event:str, team: str, include_metadata:bool = False):
    key = f"/{year}/{event}/{team}"
    response = clean_response(get(key, update = False, from_tba=False))
    return response

@app.get("/{year}/{event}")
def read_item(year:int, event:str):
    key = f"/{year}/{event}"
    response = get_from_index(key)
    return response

@app.on_event("startup")
@repeat_every(seconds=TBA_POLLING_INTERVAL)
def update_database():
    if TBA_POLLING:
        analysis.update()


