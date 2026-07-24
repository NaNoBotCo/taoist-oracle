"""Yijing 易經 — casting a hexagram by yarrow stalks or by three coins.

Both produce six lines valued 6/7/8/9 (bottom to top), but with different odds —
the one point of real statistical interest between the methods:

    line            yarrow (stalks)   three coins
    6 old yin        1/16  =  6.25%    2/16 = 12.5%
    7 young yang     5/16  = 31.25%    6/16 = 37.5%
    8 young yin      7/16  = 43.75%    6/16 = 37.5%
    9 old yang       3/16  = 18.75%    2/16 = 12.5%

Both methods give the SAME 50/50 yin/yang balance and the SAME 25% chance that
any line is moving. What the coin method changes is only the internal lean:
yarrow biases toward stable young-yin and, among moving lines, toward old-yang
(yang giving way to yin) by 3:1. Coins flatten that asymmetry to symmetric —
old yin and old yang become equally likely. See LINE_PROBS / odds_table().
"""

import random
from core import bagua

# Per-line probability of each value, by method. These are exact.
LINE_PROBS = {
    "coin":   {6: 1 / 8,  7: 3 / 8,  8: 3 / 8,  9: 1 / 8},
    "yarrow": {6: 1 / 16, 7: 5 / 16, 8: 7 / 16, 9: 3 / 16},
}
# cumulative distribution for the yarrow draw
_YARROW_CDF = [(6, 1 / 16), (7, 6 / 16), (8, 13 / 16), (9, 1.0)]


def coin_line(rng):
    """Three coins: heads(yang)=3, tails(yin)=2. Sum 6..9 -> line value.
    Gives the exact coin distribution 1/8, 3/8, 3/8, 1/8."""
    return sum(3 if rng.random() < 0.5 else 2 for _ in range(3))


def yarrow_line(rng):
    """A line drawn from the traditional yarrow-stalk distribution
    (1/16, 5/16, 7/16, 3/16 for 6/7/8/9).

    Sampling each line directly from that distribution is mathematically
    equivalent to the idealized 49-stalk rite and reproduces its historical
    bias exactly — cleaner than simulating the physical split, which only
    approximates these odds."""
    r = rng.random()
    for value, cum in _YARROW_CDF:
        if r < cum:
            return value
    return 9


def odds_table():
    """Rows for display: (value, label_zh, label_en, yarrow_pct, coin_pct)."""
    labels = {6: ("老陰", "old yin (moving)"), 7: ("少陽", "young yang"),
              8: ("少陰", "young yin"), 9: ("老陽", "old yang (moving)")}
    rows = []
    for v in (9, 8, 7, 6):
        zh, en = labels[v]
        rows.append((v, zh, en, LINE_PROBS["yarrow"][v] * 100,
                     LINE_PROBS["coin"][v] * 100))
    return rows


def cast(method="coin", rng=None):
    """Cast six lines bottom-to-top. method in {'coin','yarrow'}.
    Returns a dict describing the reading."""
    rng = rng or random.Random()
    line_fn = yarrow_line if method == "yarrow" else coin_line
    values = [line_fn(rng) for _ in range(6)]
    return reading_from_values(values, method)


def reading_from_values(values, method="given"):
    primary = bagua.Hexagram(bagua.bits_of(values))
    moving = bagua.moving_positions(values)
    result = {
        "method": method,
        "values": values,
        "primary": primary,
        "moving": moving,
        "changed": None,
    }
    if moving:
        result["changed"] = bagua.Hexagram(bagua.transform_bits(values))
    return result
