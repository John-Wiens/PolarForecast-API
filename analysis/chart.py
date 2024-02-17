class Chart():
    def __init__(self, name:str, fields: list):
        self.name = name
        self.fields = fields

class ChartField():
    def __init__(self, key:str, display_text:str=None):
        self.key = key

        if display_text is not None:
            self.display_text = display_text
        else:
            display_text = key

    