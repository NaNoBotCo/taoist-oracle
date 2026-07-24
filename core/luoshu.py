"""Luoshu 洛書 — the 3x3 magic square and its 'flying' order.

Part of the spine for the future feng-shui layer (Flying Star, Eight Mansions).
Included now so those methods drop in without touching the other core modules.
"""

# The Luoshu square, rows top-to-bottom, cols left-to-right (S at top by
# convention). Every row, column, and diagonal sums to 15.
SQUARE = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]

# Order in which stars "fly" through the nine palaces (the path of 1..9).
FLYING_ORDER = [5, 6, 7, 8, 9, 1, 2, 3, 4]  # center, NW, W, NE, S, N, SW, E, SE


def magic_sum():
    return 15


def flatten():
    return [n for row in SQUARE for n in row]
