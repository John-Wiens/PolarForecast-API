from config import MATCH_SANITIZATION
from games.frc_game import FRCGame
from data.data import get, store
from analysis.solver import smart_solve

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
        

        self.tba_matches = None
        self.data_integrity_check = "unknown"

    def update(self):
        print(f"Updating Event {self.year}{self.event_key}")
        self.tba_matches = get(self.matches_request_base.format(self.year, self.event_key), from_tba=True)
        self.tba_teams = get(self.teams_request_base.format(self.year, self.event_key), from_tba=True)


        matches = self.get_sanitized_matches()
        teams = self.get_team_lookup()

        smart_solve_stats = self.get_stat_names(self.get_stats_by_solver("smart_solve"))
        smart_solve(matches,teams,smart_solve_stats)


    def get_sanitized_matches(self):
        if MATCH_SANITIZATION:
            good_matches = []
            for match in self.tba_matches:
                if self.game.validate_match(match):
                    good_matches.append(match)
                
            if len(good_matches) < 0.9 * len(self.tba_matches):
                print("Event {self.year}{self.event_key} has failed to achieve 90% Data integrity. Predictions may be off.")
                self.data_integrity_check = "failed"
            return good_matches
        else:
            return self.tba_matches



    # Converts TBA Team listing into a dictonary mapping team keys to index's. 
    def get_team_lookup(self):
        team_lookup = {}
        index = 0
        for team in self.tba_teams['data']:
            team_lookup[team['key']] = {'index':index}
            index +=1

        return team_lookup


    # Returns a list of stats that use the given solution strategy
    def get_stats_by_solver(self, solver):
        stats = []
        for stat in self.game.stats:
            if stat.solve_strategy == solver:
                stats.append(stat)
        return stats


    def get_stat_names(self, stats):
        names = []
        for stat in stats:
            names.append(stat.stat_key)


