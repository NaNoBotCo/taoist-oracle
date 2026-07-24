"""Ganzhi 干支 — the sexagenary cycle and the four pillars.

10 Heavenly Stems x 12 Earthly Branches -> a 60-cycle. Day and hour pillars are
pure modular arithmetic; year and month pillars are bounded by solar terms
(立春 for the year, the 12 minor terms for the month).
"""

import math
from core import wuxing
from core import calendar_cn as cal

STEMS = [
    ("甲", "Jiǎ"), ("乙", "Yǐ"), ("丙", "Bǐng"), ("丁", "Dīng"), ("戊", "Wù"),
    ("己", "Jǐ"), ("庚", "Gēng"), ("辛", "Xīn"), ("壬", "Rén"), ("癸", "Guǐ"),
]
BRANCHES = [
    ("子", "Zǐ", "Rat"), ("丑", "Chǒu", "Ox"), ("寅", "Yín", "Tiger"),
    ("卯", "Mǎo", "Rabbit"), ("辰", "Chén", "Dragon"), ("巳", "Sì", "Snake"),
    ("午", "Wǔ", "Horse"), ("未", "Wèi", "Goat"), ("申", "Shēn", "Monkey"),
    ("酉", "Yǒu", "Rooster"), ("戌", "Xū", "Dog"), ("亥", "Hài", "Pig"),
]

# element of each stem: stems run Wood,Wood,Fire,Fire,Earth,Earth,Metal,Metal,Water,Water
STEM_ELEMENT = [s // 2 for s in range(10)]   # matches wuxing WOOD..WATER
BRANCH_ELEMENT = [
    wuxing.WATER, wuxing.EARTH, wuxing.WOOD, wuxing.WOOD, wuxing.EARTH,
    wuxing.FIRE, wuxing.FIRE, wuxing.EARTH, wuxing.METAL, wuxing.METAL,
    wuxing.EARTH, wuxing.WATER,
]

# The day sixty-cycle is anchored so that 2000-01-07 (CST) = 甲子 (index 0),
# a standard published reference day. Everything else counts from it.
_DAY_ANCHOR = cal._midnight_jd(2000, 1, 7)


class Pillar:
    def __init__(self, index):
        self.index = index % 60
        self.stem = self.index % 10
        self.branch = self.index % 12

    @property
    def element(self):          # the pillar's element is taken from its stem
        return STEM_ELEMENT[self.stem]

    @property
    def branch_element(self):
        return BRANCH_ELEMENT[self.branch]

    def name(self, lang="zh"):
        if lang == "zh":
            return STEMS[self.stem][0] + BRANCHES[self.branch][0]
        return f"{STEMS[self.stem][1]} {BRANCHES[self.branch][1]}"

    def animal(self):
        return BRANCHES[self.branch][2]

    def __repr__(self):
        return f"<Pillar {self.name('zh')} ({self.name('en')})>"


def _day_index(year, month, day):
    n = round(cal._midnight_jd(year, month, day) - _DAY_ANCHOR)
    return n % 60


def day_pillar(year, month, day):
    return Pillar(_day_index(year, month, day))


def hour_branch_of(hour):
    """Earthly-branch index for a clock hour 0..23 (子 = 23:00-01:00)."""
    return ((hour + 1) // 2) % 12


def hour_pillar(day_pillar_, hour):
    """Hour pillar via 五鼠遁: the 子-hour stem is fixed by the day stem."""
    branch = hour_branch_of(hour)
    stem = ((day_pillar_.stem % 5) * 2 + branch) % 10
    # index that has this (stem, branch)
    idx = _combine(stem, branch)
    return Pillar(idx)


def _combine(stem, branch):
    """Sexagenary index from a (stem, branch) pair (they must be compatible)."""
    for i in range(60):
        if i % 10 == stem and i % 12 == branch:
            return i
    raise ValueError("incompatible stem/branch")


def year_pillar(year, month, day):
    """Solar year pillar, boundary at 立春 (315 deg)."""
    lichun = cal.solar_term_jd(315, cal.gregorian_to_jd(year, 2, 1)) + cal.CST
    y = year
    if cal._midnight_jd(year, month, day) < cal._midnight_jd(*cal.jd_to_civil_date(lichun - cal.CST)):
        y -= 1
    idx = (y - 4) % 60
    return Pillar(idx)


def month_pillar(year, month, day, hour=12):
    """Month pillar from the Sun's longitude (寅 month begins at 立春, 315 deg).
    Stem via 五虎遁 from the year stem."""
    jd = cal.gregorian_to_jd(year, month, day, hour)
    lon = cal.solar_longitude(jd)
    # branch index in 子=0 numbering; 寅(=2) begins the run at 315 deg
    branch = (int(((lon - 315) % 360) // 30) + 2) % 12
    yp = year_pillar(year, month, day)
    order = (branch - 2) % 12
    stem = ((yp.stem % 5) * 2 + 2 + order) % 10
    return Pillar(_combine(stem, branch))


def void_branches(day_pillar_):
    """The two 旬空 (empty) branches of the day pillar's decade."""
    decade_start = day_pillar_.index - (day_pillar_.index % 10)
    covered = {(decade_start + i) % 12 for i in range(10)}
    return sorted(set(range(12)) - covered)


def four_pillars(year, month, day, hour):
    """Convenience: all four pillars for a moment."""
    dp = day_pillar(year, month, day)
    return {
        "year": year_pillar(year, month, day),
        "month": month_pillar(year, month, day, hour),
        "day": dp,
        "hour": hour_pillar(dp, hour),
    }
