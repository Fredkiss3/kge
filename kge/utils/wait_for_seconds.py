
import time

class WaitForSeconds:
    """
    TODO
    """
    def __init__(self, seconds: float):
        if not isinstance(seconds, (int, float)):
            raise TypeError("seconds should be a number")