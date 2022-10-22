


# Class to Encapsulate the possible ways that a given metric can be solved for. 
class Stat():
    def __init__(self, stat_key, var_name = None, solve_strategy='unlinked', display_name=None, report_stat = False):
        self.stat_key = stat_key
        
        self.solve_strategy = solve_strategy
        self.report_stat = report_stat
        
        if display_name is None:
            self.display_name = stat_key
        else:
            self.display_name = display_name

        if var_name is None:
            self.var_name = stat_key

        

