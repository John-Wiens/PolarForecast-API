


# Class to Encapsulate the possible ways that a given metric can be solved for. 
class Stat():
    def __init__(self, stat_key, var_name = None, solve_strategy='smart_solve', display_name=None, report_stat = False):
        self.stat_key = stat_key
        
        self.solve_strategy = solve_strategy
        self.report_stat = report_stat
        
        if display_name is None:
            self.display_name = stat_key
        else:
            self.display_name = display_name

        if var_name is None:
            self.var_name = stat_key

# Linked stats are a subset of stat. They are used for connecting metrics that are directly linked to robots with the appropriate robots.
# These types of stats are not solved for.
class LinkedStat(Stat):
    def __init__(self, stat_key:str, linked_key:str, mapper:dict, var_name:str = None, display_name:str=None, report_stat:str = False):
        super().__init__(stat_key, var_name=var_name, solve_strategy='linked', display_name = display_name, report_stat = report_stat)
        self.linked_key = linked_key #The key prefix used for linking this stat, does not include the robot number. EG. taxiRobot1 -> taxRobot
        self.mapper = mapper # dictionary mapping strings to numeric values

# Subclass of Stat, used for computing metrics that are the sum of other metrics. This is so common a shorthand class was made for it. 
class SumStat(Stat):
    def __init__(self, stat_key:str, component_stats:list, var_name:str = None, display_name:str=None, report_stat:str = False):
        super().__init__(stat_key, var_name=var_name, solve_strategy='aggregate', display_name = display_name, report_stat = report_stat)
        self.component_stats = component_stats


# Subclass of Stat, used for computing custom metrics based on an arbitrary function. 
class CustomStat(Stat):
    def __init__(self, stat_key:str, solve_function, var_name:str = None, display_name:str=None, report_stat:str = False):
        super().__init__(stat_key, var_name=var_name, solve_strategy='custom', display_name = display_name, report_stat = report_stat)
        self.solve_function = solve_function

    def solve_function(matches, teams):
        pass



