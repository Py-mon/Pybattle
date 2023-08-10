from copy import deepcopy

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from pybattle.screen.frames.map import Map
from pybattle.screen.grid.cell import Cell
from pybattle.screen.grid.matrix import Matrix
from pybattle.screen.grid.point import Coord, Point, Size


def _get_path(start: Point, end: Point, map_: Matrix, thick_barriers: bool = True):
    neighs = start.neighbors + end.neighbors

    for row in deepcopy(map_.dct_rows):
        for coord, cell in row.items():
            if not (cell.collision is True and coord not in neighs):
                continue
            for neigh1 in coord.neighbors:
                if thick_barriers:
                    for neigh in neigh1.neighbors:
                        try:
                            m1[neigh].collision = True
                        except IndexError:
                            pass
                else:
                    # print('HERE')
                    try:
                        m1[neigh1].collision = True
                    except IndexError:
                        pass

    matrix = [[cell.collision for cell in row] for row in map_.rows]

    grid = Grid(matrix=matrix, inverse=True)

    start_ = grid.node(*start.reversed)
    end_ = grid.node(*end.reversed)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, *_ = finder.find_path(start_, end_, grid)

    print(grid.grid_str(path, start, end))

    return [
        Coord(pos[1], pos[0]) for pos in path + [(*start.reversed,), (*end.reversed,)]
    ]


def get_path(start: Point, end: Point, map_: Matrix):
    r1 = _get_path(start, end, map_, False)
    if len(r1) <= 2:
        return _get_path(start, end, map_, True)
    return r1


# TODO pip install pybattle and fix version and fix screen. instead of pybattle.screen


m1 = Matrix(
    Cell.from_str(
        """\
╭─ BEDROOM ─┬──────────────────╮
│   ╰───────╯       ||||       │
│                   ||||       │
│                     ─┬─┬─┬─┬─┤
│                              │
│                              │
│╭│╮   ╶─╮                     │
││││    ░│                     │
│╰│╯   ╶─╯           ╭─────┬─╮ │
│                    │░░░░░│▓│ │
│                    ╰─────┴─╯ │
╰──────────────────────────────╯"""
    )
)
from time import time

s = time()
for _ in range(1):
    path = get_path(Coord(1, 19), Coord(7, 25), m1)

print(time() - s)

print(path)
for pos in path:
    m1[pos].value = "x"

print(m1)


# for pos in path:
#     m1[Coord(pos[1], pos[0])].value = "x"

# print(m1)
