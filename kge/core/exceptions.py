
class ComponentDoesNotExists(Exception):
    def __init__(self, m: str):
        super(ComponentDoesNotExists, self).__init__(m)