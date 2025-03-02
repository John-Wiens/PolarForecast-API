from config import MATCH_SANITIZATION
from games.frc_game import FRCGame
from data.data import get, store, get_year_event_matches_tba, get_year_event_teams_tba, get_year_event_rankings_tba, store_year_event_team, add_search_key, store_match_prediction, team_key_base
from analysis.solver import smart_solve, linked_solve, sum_solve, SMART_SOLVER, LINKED_SOLVER, SUM_SOLVER, CUSTOM_SOLVER, POST_SOLVER
from data.datacache import get_data_matching_key
from datetime import datetime

class Event():

    year: int
    event_key: str
    game: FRCGame

    def __init__(self, tba_event:dict, game:FRCGame):
        self.tba_event = tba_event
        self.year = tba_event.get('year',0)
        self.event_key = tba_event.get('event_code','')
        self.game = game()
        self.tba_matches = None
        self.data_integrity_check = "unknown"
        self.page = f"/data/event/{self.year}/{self.event_key}"
        
        
        
        add_search_key(f"{self.year}{self.event_key}",f"{self.year} {tba_event.get('name','')} [{self.event_key}]", self.page, tba_event.get('start_date',None), tba_event.get('end_date', None))

    def create_search_keys(self):
        self.tba_event_info = get_year_event_matches_tba(self.year, self.event_key)

    def get_as_date(self, date):
        if(date != ''):
            return datetime.strptime(date, '%Y-%m-%d')
        else:
            return None

    def update(self):
        print(f"Updating Event {self.year}{self.event_key}")
        self.tba_matches = get_year_event_matches_tba(self.year, self.event_key)
        print(f"    Retrieved {len(self.tba_matches)} Matches.")
        self.tba_teams = get_year_event_teams_tba(self.year, self.event_key)
        print(f"    Retrieved {len(self.tba_teams)} Teams.")
        self.tba_rankings = get_year_event_rankings_tba(self.year, self.event_key)
        print(f"    Retrieved Rankings.")
        self.teams = self.update_team_info()
        print(f"    Updated {len(self.teams)} Teams.")
        self.update_match_predictions()
        print(f"    Updated Match Predictions.")
        # self.ml()

    def ml(self):
        with open('ml.csv', 'w') as ml:
            count = 0
            for match in self.tba_matches:
                count +=1
                for team_key in match.get('alliances',{}).get('blue',{}).get('team_keys',[]):
                    auto = self.teams.get(team_key,{}).get('auto',0)
                    cargo = self.teams.get(team_key,{}).get('cargo',0)
                    endgame = self.teams.get(team_key,{}).get('endgame',0)
                    ml.write(f'{auto},{cargo},{endgame},')
                    

                for team_key in match.get('alliances',{}).get('red',{}).get('team_keys',[]):
                    auto = self.teams.get(team_key,{}).get('auto',0)
                    cargo = self.teams.get(team_key,{}).get('cargo',0)
                    endgame = self.teams.get(team_key,{}).get('endgame',0)
                    ml.write(f'{auto},{cargo},{endgame},')




                blue_score = match['score_breakdown']['blue']['totalPoints']
                red_score = match['score_breakdown']['red']['totalPoints']
                ml.write(f'{blue_score},{red_score}\n')

    # Update Team Performances Based on Latest available TBA Data
    def update_team_info(self):
        matches = self.get_sanitized_matches(self.tba_matches)
        played_matches = self.get_played_matches(matches)
        teams = self.create_team_lookup(self.tba_teams, self.tba_rankings, matches)
        if len(teams) == 0:
            return teams

        for preprocessor in self.game.preprocessors:
            played_matches, teams = preprocessor(played_matches, teams)

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
            elif stat.solve_strategy == POST_SOLVER:
                teams = stat.solve_function(matches, teams, stat, self.tba_rankings)
                pass
            else:
                print("Unable to Solve Stat:", stat.stat_key, "Unknown Solution Strategy", stat.solve_strategy )
        
        self.save_team_stats(teams, self.game.stats)
        return teams

    def update_match_predictions(self):
        matches = {}
        for match in self.tba_matches:
            prediction = self.game.predict_match(match, self.teams)
            store_match_prediction(self.year, self.event_key, prediction.get('key',''), prediction)

    def save_team_stats(self, teams, stats):
        for team in teams:
            store_year_event_team(self.year, self.event_key, team, teams[team])

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
            #print("\n\n",matches)
            result_time = match.get("post_result_time",-1)
            #if result_time is not None and result_time > 0: #and match['comp_level'] == 'qm'
            if match.get("alliances",{}).get('blue',{}).get('score',-1) >= 0:
                played_matches.append(match)
        return played_matches



    # Converts TBA Team listing into a dictonary mapping team keys to index's.
    # Adds in Team keys to the mapping to preserve data when compressed to list
    # Add in Rankings
    def create_team_lookup(self, teams, rankings, matches):
        team_lookup = {}
        index = 0
        teams_in_matches = self.get_teams_from_matches(matches)
        team_keys = [ t['key'] for t in teams ]
        for team in teams_in_matches:
            if team not in team_keys:
                teams.append(self.gen_simple_team_record(team))
        event_day = self.get_as_date(self.tba_event.get('start_date'))
        load_historical = not (self.get_as_date(self.tba_event.get('end_date')) < datetime.now())
        
        for team in teams:
            if load_historical:
                previous_events = get_data_matching_key(team_key_base.format(year=self.year, event="*", team = team['key']))
            else:
                previous_events = []
            
            latest_date = datetime(self.year, 1, 1)
            latest_event = None
            for event in previous_events:
                comp_date = self.get_as_date(event.get('_end_date',''))
                valid_import = event.get('_valid_import',  True)
                if not valid_import:
                    continue
                if comp_date != None and comp_date > latest_date and comp_date < event_day:
                    latest_date = comp_date
                    latest_event = event
            if latest_event != None:
                del latest_event['metadata']
                team_lookup[team['key']] = latest_event
                team_lookup[team['key']]['historical'] = True

            else:
                team_lookup[team['key']] = {'historical': False}

            team_lookup[team['key']]['key'] = team['key']
            team_lookup[team['key']]['_index'] = index
            team_lookup[team['key']]['_event'] = self.tba_event.get('event_code')
            team_lookup[team['key']]['_start_date'] = self.tba_event.get('start_date','')
            team_lookup[team['key']]['_end_date'] = self.tba_event.get('end_date','')

            if len(self.tba_matches) < 17:
                team_lookup[team['key']]['_valid_import'] = False
            else:
                team_lookup[team['key']]['_valid_import'] = True
            index +=1

        

        return team_lookup
    def get_teams_from_matches(self, matches):
        teams = set()
        for match in matches:
            blue = match.get('alliances',{}).get('blue').get('team_keys',[])
            red = match.get('alliances',{}).get('red').get('team_keys',[])
            for elem in (red + blue):
                teams.add(elem)
        return teams

    def gen_simple_team_record(self, key):
        return {'address': None, 'city': '', 'country': '', 'gmaps_place_id': None, 'gmaps_url': None, 'key': key, 'lat': None, 'lng': None, 'location_name': None, 'motto': None, 'name': '', 'nickname': '', 'postal_code': '', 'rookie_year': 0, 'school_name': '', 'state_prov': '', 'team_number': key[4:], 'website': ''}

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


