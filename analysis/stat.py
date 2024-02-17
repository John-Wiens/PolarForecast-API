

from analysis.solver import SMART_SOLVER, LINKED_SOLVER, SUM_SOLVER, CUSTOM_SOLVER, POST_SOLVER


# Class to Encapsulate the possible ways that a given metric can be solved for. 
class Stat():
    def __init__(self, stat_key, solve_strategy=SMART_SOLVER, display_name=None, report_stat = False, order = -1):
        self.stat_key = stat_key
        
        self.solve_strategy = solve_strategy
        self.report_stat = report_stat
        self.order = order
        
        if display_name is None:
            self.display_name = stat_key
        else:
            self.display_name = display_name

    def get_stat_description(self) -> dict:
        return {
            "stat_key": self.stat_key,
            "solve_strategy": self.solve_strategy,
            "report_stat": self.report_stat,
            "display_name": self.display_name,
            "stat": self.get_stat_specific_description(),
            "order": self.order
        }

    def get_stat_specific_description(self) -> dict:
        return {}

# Linked stats are a subset of stat. They are used for connecting metrics that are directly linked to robots with the appropriate robots.
# These types of stats are not solved for.
class LinkedStat(Stat):
    def __init__(self, stat_key:str, linked_key:str, mapper:dict, display_name:str=None, report_stat:str = False):
        super().__init__(stat_key, solve_strategy=LINKED_SOLVER, display_name = display_name, report_stat = report_stat)
        self.linked_key = linked_key #The key prefix used for linking this stat, does not include the robot number. EG. taxiRobot1 -> taxRobot
        self.mapper = mapper # dictionary mapping strings to numeric values
    
    

# Subclass of Stat, used for computing metrics that are the sum of other metrics. This is so common a shorthand class was made for it. 
class SumStat(Stat):
    def __init__(self, stat_key:str, component_stats:list, weights:list = None, display_name:str=None, report_stat:str = False, order=-1):
        super().__init__(stat_key, solve_strategy=SUM_SOLVER, display_name = display_name, report_stat = report_stat, order=order)
        self.component_stats = component_stats
        
        if weights is None:
            weights = [1 for x in range(0, len(component_stats))]
        elif len(weights) == len(component_stats):
            self.weights = weights
        else:
            print(f"Provided Weights does not match length of Provided compoents for Stat: {self.stat_key}")

        self.weights = weights

    def get_stat_specific_description(self) -> dict:
        return {
            "component_stats": self.component_stats
        }

# Subclass of Stat, used for computing custom metrics based on an arbitrary function. 
class CustomStat(Stat):
    def __init__(self, stat_key:str, solve_function, display_name:str=None, report_stat:str = False, order=-1):
        super().__init__(stat_key, solve_strategy=CUSTOM_SOLVER, display_name = display_name, report_stat = report_stat, order=order)
        self.solve_function = solve_function

    def solve_function(matches, teams):
        pass

class PostStat(Stat):
    def __init__(self, stat_key:str, solve_function, display_name:str=None, report_stat:str = False, order=-1):
        super().__init__(stat_key, solve_strategy=POST_SOLVER, display_name = display_name, report_stat = report_stat, order=order)
        self.solve_function = solve_function

    def solve_function(matches, teams):
        pass


class RankStat(Stat):
    def __init__(self, stat_key:str, solve_function, display_name:str=None, report_stat:str = False, order=-1):
        super().__init__(stat_key, solve_strategy=CUSTOM_SOLVER, display_name = display_name, report_stat = report_stat, order=order)
        self.solve_function = solve_function


