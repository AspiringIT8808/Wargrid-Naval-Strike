"""Tiny coordinate helpers. A cell is a (row, col) tuple."""
from rules.config import GRID


def in_bounds(cell):
    return 0 <= cell[0] < GRID and 0 <= cell[1] < GRID


def cell_name(cell):
    return f"{chr(65 + cell[1])}{cell[0] + 1}"          # (0, 0) -> "A1"


def cell_from_name(name):
    """"A1" -> (0, 0). The reverse of cell_name(), used to turn a log line
    like 'fires at L12' back into a board cell for the floating-text popup."""
    return (int(name[1:]) - 1, ord(name[0].upper()) - 65)


def line_cells(anchor, size, horizontal):
    r, c = anchor
    return [(r, c + i) if horizontal else (r + i, c) for i in range(size)]


def area_cells(center, n):
    """n x n block around center (clipped to the board)."""
    off = (n - 1) // 2
    r, c = center
    return [(rr, cc) for rr in range(r - off, r - off + n)
            for cc in range(c - off, c - off + n) if in_bounds((rr, cc))]
