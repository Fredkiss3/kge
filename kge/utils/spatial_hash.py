import logging
from collections import defaultdict
from typing import Any, Type, Dict, Set

from math import floor

from kge.utils.vector import Vector

logger = logging.getLogger(__name__)


class Box:
    """
    A Box, an object used to represent bounds in the hash table
    """

    def __init__(self, center: Vector, size: Vector):
        self.center = center
        self.size = size
        self.x1, self.y1 = Vector(center - size / 2)
        self.x2, self.y2 = Vector(center + size / 2)

    def __repr__(self):
        return f'Box(center={self.center}, size={self.size})'

    def overlaps(self, other: "Box"):
        """
        Check if another box overlaps this one.
        """
        size, point = other.size, other.center

        # Minimum distances before the collision occurs
        min_dist_x = size.x / 2 + abs(self.size.x) / 2
        min_dist_y = size.y / 2 + abs(self.size.y) / 2

        # vector from the other box to self
        distVec = point - Vector(self.center.x, self.center.y)

        # depth of the collision
        # Difference between the Min Distance before a collision occurs
        # and the actual distance between the other and this one
        xDepth = min_dist_x - abs(distVec.x)
        yDepth = min_dist_y - abs(distVec.y)

        if xDepth > 0 and yDepth > 0:
            return True
        return False


class SpatialHash(object):
    def __init__(self, cell_size=10.0):
        self.cell_size = float(cell_size)
        self.table = {}

        # types
        self._kinds = defaultdict(set)

    def _add(self, cell_coord, o):
        """Add the object o to the cell at cell_coord."""
        try:
            self.table.setdefault(cell_coord, set()).add(o)
        except KeyError:
            self.table[cell_coord] = {o}

        for kind in type(o).mro():
            self._kinds[kind].add(o)

    def _cells_for_rect(self, r: Box):
        """Return a set of the cells into which r extends."""
        cells = set()
        cy = floor(r.y1 / self.cell_size)
        while (cy * self.cell_size) < r.y2:
            cx = floor(r.x1 / self.cell_size)
            while (cx * self.cell_size) < r.x2:
                cells.add((int(cx), int(cy)))
                cx += 1.0
            cy += 1.0
        return cells

    def add(self, position: Vector, size: Vector, obj: Any):
        """Add an object obj with bounds r."""
        if not isinstance(position, Vector) or not isinstance(size, Vector):
            raise TypeError("Position & Size should be vectors")

        box = Box(position, size)
        cells = self._cells_for_rect(box)
        for c in cells:
            self._add(c, obj)

    def _remove(self, cell_coord, o):
        """Remove the object o from the cell at cell_coord."""
        cell = None
        try:
            cell = self.table[cell_coord]
            cell.remove(o)
        except KeyError as e:
            logger.error(f"KeyError {e}: {cell, type(cell), cell_coord}")
        else:
            logger.debug(f"'{o}' removed from Spatial Hash")

        # Delete the cell from the hash if it is empty.
        if cell is not None:
            if not cell:
                try:
                   del (self.table[cell_coord])
                except KeyError as e:
                    logger.error(f"KeyError {e}: {cell, type(cell), cell_coord}")

    def remove(self, position: Vector, size: Vector, obj: Any):
        """Remove an object obj which had bounds r."""
        if not isinstance(position, Vector) or not isinstance(size, Vector):
            raise TypeError("Position & Size should be vectors")

        box = Box(position, size)
        cells = self._cells_for_rect(box)

        for c in cells:
            self._remove(c, obj)

    def search(self, position: Vector, size: Vector, *type_: Type):
        """Get a set of all objects in a certain area"""
        if not isinstance(position, Vector) or not isinstance(size, Vector):
            raise TypeError("Position & Size should be vectors")

        box = Box(position, size)
        cells = self._cells_for_rect(box)

        found = set()
        for c in cells:
            found.update(self.table.get(c, set()))

        # if type is given then intersect with the registered ones
        f = set()
        for t in type_:
            if t in self._kinds:
                f.update(found.intersection(self._kinds[t]))

        if type_:
            found = f

        return found


if __name__ == '__main__':
    hash = SpatialHash(2)


    #
    #
    # class Box:
    #     def __init__(self, center: Vector, size: Vector):
    #         self.x1, self.y1 = Vector(center - size / 2)
    #         self.x2, self.y2 = Vector(center + size / 2)

    # print(self.x1, self.y1, self.x2, self.y2, )

    class Obj:
        nb = 0

        def __init__(self, box: Box):
            self.box = box
            type(self).nb += 1
            self.name = f"Object {str(type(self).nb)}"

        def __repr__(self):
            return self.name

    class Entity:
        nb = 0

        def __init__(self, box: Box):
            self.box = box
            Entity.nb += 1
            self.name = f"Entity {str(Entity.nb)}"

        def __repr__(self):
            return self.name


    e = Entity(Box(Vector.Zero(), Vector(1, 1)))
    e2 = Entity(Box(Vector(-1 / 2, 1 / 2), Vector(1, 1)))
    e3 = Entity(Box(Vector(2, 2), Vector.Unit() * 2))
    e4 = Entity(Box(Vector(0, -1.5), Vector(2, 1)))
    e5 = Entity(Box(Vector(-3, 0), Vector(1, 2)))

    o1 = Obj(Box(Vector.Zero(), Vector.Unit()))
    o2 = Obj(Box(Vector(-3, 0), Vector(1, 2)))

    ls = [e, e2, e3, e4, e5, o2, o1]

    # e2 = Entity(Box(Vector.Unit() * 4, Vector(1, 1)))
    for e_ in ls:
        hash.add(e_.box.center, e_.box.size, e_)
    # hash.add_rect(e2.box, e2)

    # print(hash.potential_collisions(e2.box, e2))

    for cell, entities in hash.table.items():
        print(cell, ":", entities)

    region = Box(Vector(.5, .5), Vector.Unit() / 2)
    print(hash.search(region.center, region.size, Entity, Obj))
