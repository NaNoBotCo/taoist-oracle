"""Liu Yao 六爻 / Wen Wang Gua 文王卦 — the coin hexagram with its full overlay.

The cast is a plain three-coin hexagram. What makes Liu Yao its own method is
the deterministic scaffolding hung on the six lines: each line gets an Earthly
Branch (纳甲 najia) and thus an element, a 'six relative' relation to the
hexagram's palace element, a world/response mark (世/應), and a 'six beast'
(六獸) set by the day's stem. The day's void branches (旬空) are also flagged.
"""

import random
from core import bagua, wuxing, ganzhi

# --- Najia 纳甲: Earthly-branch index per trigram, lines bottom->top -----------
# Lower trigram of a hexagram uses the 'inner' set; upper uses the 'outer' set.
NAJIA = {
    0: ((0, 2, 4),  (6, 8, 10)),    # 乾 Qian  子寅辰 / 午申戌
    1: ((5, 3, 1),  (11, 9, 7)),    # 兌 Dui   巳卯丑 / 亥酉未
    2: ((3, 1, 11), (9, 7, 5)),     # 離 Li    卯丑亥 / 酉未巳
    3: ((0, 2, 4),  (6, 8, 10)),    # 震 Zhen  子寅辰 / 午申戌
    4: ((1, 11, 9), (7, 5, 3)),     # 巽 Xun   丑亥酉 / 未巳卯
    5: ((2, 4, 6),  (8, 10, 0)),    # 坎 Kan   寅辰午 / 申戌子
    6: ((4, 6, 8),  (10, 0, 2)),    # 艮 Gen   辰午申 / 戌子寅
    7: ((7, 5, 3),  (1, 11, 9)),    # 坤 Kun   未巳卯 / 丑亥酉
}

# --- Eight Houses 八宮: which pure-trigram palace each hexagram belongs to -----
# Flip sets (1-indexed lines) that generate the 8 members of a palace.
_POS_FLIPS = [set(), {1}, {1, 2}, {1, 2, 3}, {1, 2, 3, 4}, {1, 2, 3, 4, 5},
              {1, 2, 3, 5}, {5}]
_WORLD_LINE = [6, 1, 2, 3, 4, 5, 4, 3]   # 世 line per palace position


def _build_palace_map():
    """hexagram number -> (palace_trigram_index, position 0..7)."""
    out = {}
    for t in range(8):
        head = list(bagua.TRIGRAMS[t][4]) * 2      # doubled trigram, 6 bits
        for pos, flips in enumerate(_POS_FLIPS):
            bits = tuple(1 - head[i] if (i + 1) in flips else head[i]
                         for i in range(6))
            num = bagua.hexagram_number(bits)
            out[num] = (t, pos)
    return out


PALACE = _build_palace_map()

BEASTS = ["青龍", "朱雀", "勾陳", "螣蛇", "白虎", "玄武"]
BEASTS_EN = ["Azure Dragon", "Vermilion Bird", "Hooked Array",
             "Soaring Serpent", "White Tiger", "Dark Warrior"]
# starting line-1 beast index by day stem
_BEAST_START = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 3, 6: 4, 7: 4, 8: 5, 9: 5}


def _line_branches(hexagram):
    """Six branch indices, line 1..6 (bottom to top)."""
    lower_inner = NAJIA[hexagram.lower][0]
    upper_outer = NAJIA[hexagram.upper][1]
    return list(lower_inner) + list(upper_outer)


def analyze(hexagram, year, month, day, hour, palace_element=None):
    """Full Liu Yao overlay for a hexagram cast on a given date/time.

    palace_element, if given, overrides the hexagram's own palace element when
    assigning the six relatives — used for the changed hexagram, whose lines are
    read against the ORIGINAL hexagram's palace by convention."""
    dp = ganzhi.day_pillar(year, month, day)
    palace_t, pos = PALACE[hexagram.number]
    own_palace_el = bagua.TRIGRAMS[palace_t][5]
    palace_el = own_palace_el if palace_element is None else palace_element
    world = _WORLD_LINE[pos]
    response = ((world + 3 - 1) % 6) + 1
    void = set(ganzhi.void_branches(dp))
    beast0 = _BEAST_START[dp.stem]
    branches = _line_branches(hexagram)

    lines = []
    for i in range(6):
        br = branches[i]
        el = ganzhi.BRANCH_ELEMENT[br]
        rel = wuxing.relation(palace_el, el)
        lines.append({
            "pos": i + 1,
            "branch": br,
            "branch_name": ganzhi.BRANCHES[br][0],
            "element": el,
            "relative": wuxing.SIX_RELATIVES[rel],
            "world": (i + 1) == world,
            "response": (i + 1) == response,
            "void": br in void,
            "beast": BEASTS[(beast0 + i) % 6],
            "beast_en": BEASTS_EN[(beast0 + i) % 6],
        })
    return {
        "palace": bagua.TRIGRAMS[palace_t],
        "palace_element": palace_el,
        "world": world,
        "response": response,
        "day_pillar": dp,
        "void_branches": [ganzhi.BRANCHES[b][0] for b in sorted(void)],
        "lines": lines,
    }


def cast(year, month, day, hour, rng=None):
    """Cast a Wen Wang Gua for the given moment. Returns the hexagram reading
    plus the Liu Yao overlay for both primary and changed hexagrams."""
    from methods import yijing
    rng = rng or random.Random()
    reading = yijing.cast(method="coin", rng=rng)
    reading["overlay"] = analyze(reading["primary"], year, month, day, hour)
    if reading["changed"]:
        # changed lines are read against the ORIGINAL hexagram's palace
        reading["overlay_changed"] = analyze(
            reading["changed"], year, month, day, hour,
            palace_element=reading["overlay"]["palace_element"])
    return reading
