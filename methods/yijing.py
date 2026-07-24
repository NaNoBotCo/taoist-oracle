"""Yijing 易經 — casting a hexagram by yarrow stalks or by three coins.

Both produce six lines valued 6/7/8/9 (bottom to top). The two methods differ
in their odds: the coin method is uniform per coin; the yarrow procedure biases
toward stable lines, the classic difference practitioners care about.
"""

import random
from core import bagua


def coin_line(rng):
    """Three coins: heads(yang)=3, tails(yin)=2. Sum 6..9 -> line value."""
    return sum(3 if rng.random() < 0.5 else 2 for _ in range(3))


def yarrow_line(rng):
    """The traditional three-fold division of 49 stalks.

    Each round splits the heap, sets one stalk aside, and removes the two heaps'
    remainders (mod 4, counting 0 as 4). After three rounds the remaining
    stalks divided by four give 6, 7, 8, or 9 — with the historical bias
    (8 and 7 common, 6 and 9 rare)."""
    stalks = 49
    for _ in range(3):
        left = rng.randint(2, stalks - 2)
        right = stalks - left - 1          # one stalk set between the fingers
        lr = left % 4 or 4
        rr = right % 4 or 4
        stalks -= (1 + lr + rr)
    return stalks // 4


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
