
import time

class WaitForSeconds:
    """
    Waiting for seconds
    """
    def __init__(self, seconds: float):
        dt = time.time()
        while time.time() - seconds <= dt:
            continue

if __name__ == '__main__':

    print("Start...")
    WaitForSeconds(.4)
    print("End !")