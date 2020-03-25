from math import floor


class HashMap(object):
    """
    Hashmap is a a spatial index which can be used for a broad-phase
    collision detection strategy.
    """

    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = {}

    @classmethod
    def from_points(cls, cell_size, points):
        """
        Build a HashMap from a list of points.
        """
        hashmap = cls(cell_size)
        setdefault = hashmap.grid.setdefault
        key = hashmap.key
        for point in points:
            setdefault(key(point), []).append(point)
        return hashmap

    def key(self, point):
        cell_size = self.cell_size
        return (
            int((floor(point[0]/cell_size))*cell_size),
            int((floor(point[1]/cell_size))*cell_size),
            int((floor(point[2]/cell_size))*cell_size)
        )

    def insert(self, point):
        """
        Insert point into the hashmap.
        """
        self.grid.setdefault(self.key(point), []).append(point)

    def query(self, point):
        """
        Return all objects in the cell specified by point.
        """
        return self.grid.setdefault(self.key(point), [])


if __name__ == '__main__':

    from random import uniform
    from time import time

    NUM_POINTS = 100000

    def new_point():
        return uniform(-100, 100), uniform(-100, 100), uniform(-100, 100)

    points = [new_point() for i in range(NUM_POINTS)]
    T = time()
    hashmap = HashMap.from_points(10, points)
    print(1.0 / (time() - T), '%d point builds per second.' % NUM_POINTS)

    T = time()
    hashmap.query((0, 0, 0))
    print(1.0 / (time() - T), '%d point queries per second.' % NUM_POINTS)
