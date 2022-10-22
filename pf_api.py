import analysis.analysis

from config import TBA_POLLING, TBA_POLLING_INTERVAL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

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

@app.get("/events")
def read_item():
    return 501

@app.get("/teams/{team}")
def read_item(team: str):
    return 501

@app.get("/events/{event_key}")
def read_item(event_key: str):
    return 501

@app.get("/events/{event_key}/rankings")
def read_item(event_key: str):
    return 501

@app.get("/events/{event_key}/matches/{match_key}")
def read_item(event_key: str, match_key: str):
    return 501

@app.get("/events/{event_key}/matches")
def read_item(event_key: str, comp_level: str = None):
    return 501

@app.on_event("startup")
@repeat_every(seconds=TBA_POLLING_INTERVAL)
def update_database():
    if TBA_POLLING:
        analysis.update()


