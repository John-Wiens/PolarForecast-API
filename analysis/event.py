from config import MATCH_SANITIZATION
from games.frc_game import FRCGame
from data.data import get, store
from analysis.solver import smart_solve, linked_solve, sum_solve, SMART_SOLVER, LINKED_SOLVER, SUM_SOLVER, CUSTOM_SOLVER



class Event():

    year: int
    event_key: str
    game: FRCGame
    matches_request_base:str = "/event/{}{}/matches"
    teams_request_base:str = "/event/{}{}/teams"
    ranking_request_base:str = "/event/{}{}/rankings"
    team_key_base: str = "/{year}/{event}/{team}"

    def __init__(self, year:int, event_key:str, game:FRCGame):
        self.year = year
        self.event_key = event_key
        self.game = game()
        self.tba_matches = None
        self.data_integrity_check = "unknown"

    def update(self):
        print(f"Updating Event {self.year}{self.event_key}")
        self.tba_matches = get(self.matches_request_base.format(self.year, self.event_key), from_tba=True)['data']
        self.tba_teams = get(self.teams_request_base.format(self.year, self.event_key), from_tba=True)['data']        
        self.tba_rankings = get(self.ranking_request_base.format(self.year, self.event_key), from_tba=True)['data']
        self.update_team_info()

    # Update Team Performances Based on Latest available TBA Data
    def update_team_info(self):
        matches = self.get_sanitized_matches(self.tba_matches)
        played_matches = self.get_played_matches(matches)
        teams = self.create_team_lookup(self.tba_teams, self.tba_rankings)

        smart_solve_stats = self.get_stat_names(self.get_stats_by_solver(SMART_SOLVER))
        link_solve_stats = self.get_stats_by_solver(LINKED_SOLVER)
        
        # Precompute Direct Stats
        teams = smart_solve(played_matches, teams, smart_solve_stats)
        teams = linked_solve(played_matches, teams, link_solve_stats)

        for stat in self.game.stats:
            if stat.solve_strategy in [SMART_SOLVER, LINKED_SOLVER]:
                continue
            elif stat.solve_strategy == SUM_SOLVER:
                teams = sum_solve(teams, stat)
                pass
            elif stat.solve_strategy == CUSTOM_SOLVER:
                teams = stat.solve_function(played_matches, teams, stat, self.tba_rankings)
                pass
            else:
                print("Unable to Solve Stat:", stat.stat_key, "Unknown Solution Strategy", stat.solve_strategy )

        for team in teams:
            for stat in self.game.stats:
                if not stat.report_stat:
                    del teams[team][stat.stat_key]
            key = self.team_key_base.format(year = self.year, event=self.event_key, team=team)
            store(key, teams[team], index=True)

    def get_sanitized_matches(self, matches):
        if MATCH_SANITIZATION:
            good_matches = []
            for match in self.tba_matches:
                if self.game.validate_match(match):
                    good_matches.append(match)
                
            if len(good_matches) < 0.9 * len(matches):
                print("Event {self.year}{self.event_key} has failed to achieve 90% Data integrity. Predictions may be off.")
                self.data_integrity_check = "failed"
            return good_matches
        else:
            return matches

    def get_played_matches(self, matches):
        played_matches = []
        for match in matches:
            if "post_result_time" in match and match["post_result_time"] > 0:
                played_matches.append(match)
        return played_matches



    # Converts TBA Team listing into a dictonary mapping team keys to index's.
    # Adds in Team keys to the mapping to preserve data when compressed to list
    # Add in Rankings
    def create_team_lookup(self, teams, rankings):
        team_lookup = {}
        index = 0
        for team in teams:
            team_lookup[team['key']] = {'key':team['key'], '_index':index}
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
        return names


