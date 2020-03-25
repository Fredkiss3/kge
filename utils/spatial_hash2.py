from math import floor

from kge import Vector


class SpatialHash(object):
    def __init__(self, cell_size=10.0):
        self.cell_size = float(cell_size)
        self.d = {}

    def _add(self, cell_coord, o):
        """Add the object o to the cell at cell_coord."""
        try:
            self.d.setdefault(cell_coord, set()).add(o)
        except KeyError:
            self.d[cell_coord] = {o}

    def _cells_for_rect(self, r):
        """Return a set of the cells into which r extends."""
        cells = set()
        cy = floor(r.y1 / self.cell_size)
        while (cy * self.cell_size) <= r.y2:
            cx = floor(r.x1 / self.cell_size)
            while (cx * self.cell_size) <= r.x2:
                cells.add((int(cx), int(cy)))
                cx += 1.0
            cy += 1.0
        return cells

    def add_rect(self, r, obj):
        """Add an object obj with bounds r."""
        cells = self._cells_for_rect(r)
        for c in cells:
            self._add(c, obj)

    def _remove(self, cell_coord, o):
        """Remove the object o from the cell at cell_coord."""
        cell = self.d[cell_coord]
        cell.remove(o)

        # Delete the cell from the hash if it is empty.
        if not cell:
            del (self.d[cell_coord])

    def remove_rect(self, r, obj):
        """Remove an object obj which had bounds r."""
        cells = self._cells_for_rect(r)
        for c in cells:
            self._remove(c, obj)

    def potential_collisions(self, r, obj):
        """Get a set of all objects that potentially intersect obj."""
        cells = self._cells_for_rect(r)
        potentials = set()
        for c in cells:
            potentials.update(self.d.get(c, set()))
        potentials.discard(obj)  # obj cannot intersect itself
        return potentials


if __name__ == '__main__':
    hash = SpatialHash(1)


    class Box:
        def __init__(self, center: Vector, size: Vector):
            self.x1, self.y1 = Vector(center - size / 2)
            self.x2, self.y2 = Vector(center + size / 2)

            print(self.x1, self.y1, self.x2, self.y2, )


    class Entity:
        nb = 0

        def __init__(self, box: Box):
            self.box = box
            Entity.nb += 1
            self.name = f"Entity {str(Entity.nb)}"

        def __repr__(self):
            return self.name


    e = Entity(Box(Vector.Zero(), Vector(2, 2)))
    # e2 = Entity(Box(Vector.Unit() * 4, Vector(1, 1)))
    hash.add_rect(e.box, e)
    # hash.add_rect(e2.box, e2)

    # print(hash.potential_collisions(e2.box, e2))

    print(hash.d, len(hash.d))
