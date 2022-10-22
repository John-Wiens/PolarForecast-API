from config import MATCH_SANITIZATION
from games.frc_game import FRCGame
from data.data import get, store

class Event():

    year: int
    event_key: str
    game: FRCGame
    matches_request_base:str = "/event/{}{}/matches"
    teams_request_base:str = "/event/{}{}/teams"

    def __init__(self, year:int, event_key:str, game:FRCGame):
        self.year = year
        self.event_key = event_key
        self.game = game()
        

        self.matches = None
        self.data_integrity_check = "unknown"

    def update(self):
        print(f"Updating Event {self.year}{self.event_key}")
        self.matches = get(self.matches_request_base.format(self.year, self.event_key), from_tba=True)
        self.teams = get(self.teams_request_base.format(self.year, self.event_key), from_tba=True)


        
        
        
        team_lookup = self.get_team_lookup()
        unlinked_stats = self.get_stats_by_key("unlinked")
        linked_stats = self.get_stats_by_key("linked")


        




        pass


    def get_sanitized_matches(self):
        if MATCH_SANITIZATION:
            good_matches = []
            for match in self.matches:
                if self.game.validate_match(match):
                    good_matches.append(match)
                
            if len(good_matches) < 0.9 * len(self.matches):
                print("Event {self.year}{self.event_key} has failed to achieve 90% Data integrity. Predictions may be off.")
                self.data_integrity_check = "failed"
            return good_matches
        else:
            return self.matches



    # Converts TBA Team listing into a dictonary mapping team keys to index's. 
    def get_team_lookup(self):
        team_lookup = {}
        index = 0
        for team in self.teams['data']:
            team_lookup[team['key']] = {'index':index}
            index +=1

        return team_lookup


    # Returns a list of stats that use the given solution strategy
    def get_stats_by_key(self, key):
        stats = []
        for stat in self.game.stats:
            if stat.solve_strategy == key:
                stats.append(stat)

