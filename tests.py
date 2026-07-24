"""Self-tests for the spine and the cast-oracle methods. Run: python3 tests.py"""

import random
from core import bagua, ganzhi, wuxing
from core import calendar_cn as cal
from data import hexagrams
from methods import yijing, meihua, liuyao

PASS = 0
FAIL = 0


def check(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
    else:
        FAIL += 1
        print(f"  FAIL: {name}")


# --- King Wen table --------------------------------------------------------
check("64 hexagrams", len(hexagrams.KINGWEN) == 64)
check("numbers 1..64", sorted(r[0] for r in hexagrams.KINGWEN) == list(range(1, 65)))
check("trigram pairs unique", len(hexagrams.BY_TRIGRAMS) == 64)
# spot checks (lower, upper) -> number
check("Tai=11 Qian/Kun", hexagrams.BY_TRIGRAMS[(0, 7)] == 11)
check("Pi=12 Kun/Qian", hexagrams.BY_TRIGRAMS[(7, 0)] == 12)
check("JiJi=63 Li/Kan", hexagrams.BY_TRIGRAMS[(2, 5)] == 63)
check("WeiJi=64 Kan/Li", hexagrams.BY_TRIGRAMS[(5, 2)] == 64)

# --- bagua ops -------------------------------------------------------------
check("Qian all yang -> #1", bagua.Hexagram((1, 1, 1, 1, 1, 1)).number == 1)
check("Kun all yin -> #2", bagua.Hexagram((0, 0, 0, 0, 0, 0)).number == 2)
# old yin (6) -> yang, old yang (9) -> yin
check("transform 6->yang", bagua.transform_bits([6, 8, 8, 8, 8, 8])[0] == 1)
check("transform 9->yin", bagua.transform_bits([9, 7, 7, 7, 7, 7])[0] == 0)
check("moving positions", bagua.moving_positions([6, 7, 8, 9, 7, 8]) == [1, 4])

# --- ganzhi ----------------------------------------------------------------
check("anchor 2000-01-07 = 甲子", ganzhi.day_pillar(2000, 1, 7).index == 0)
check("next day advances", ganzhi.day_pillar(2000, 1, 8).index == 1)
check("60-day wrap", ganzhi.day_pillar(2000, 3, 7).index == ganzhi.day_pillar(2000, 1, 7).index)
# hour: on a 甲 day, 子 hour is 甲子
jiazi_day = ganzhi.day_pillar(2000, 1, 7)
check("五鼠遁 甲日子時=甲子", ganzhi.hour_pillar(jiazi_day, 0).name("zh") == "甲子")
# void of 甲子 decade: 戌 亥
check("旬空 of 甲子 = 戌亥", ganzhi.void_branches(jiazi_day) == [10, 11])
check("stem element mapping", ganzhi.STEM_ELEMENT[0] == wuxing.WOOD and ganzhi.STEM_ELEMENT[8] == wuxing.WATER)

# --- calendar: known Chinese New Years -------------------------------------
def is_newyear(y, m, d, ly):
    lun = cal.lunar_date(y, m, d)
    return lun["year"] == ly and lun["month"] == 1 and lun["day"] == 1 and not lun["is_leap"]

check("CNY 2023-01-22", is_newyear(2023, 1, 22, 2023))
check("CNY 2024-02-10", is_newyear(2024, 2, 10, 2024))
check("CNY 2025-01-29", is_newyear(2025, 1, 29, 2025))
# 2023 had a leap 2nd month (闰二月); a date in late March falls in it
_leap23 = any(cal.lunar_date(2023, 3, d)["is_leap"] for d in range(22, 32))
check("2023 leap month exists in Mar", _leap23)
# solar longitude near spring equinox
check("equinox ~0 deg", abs(((cal.solar_longitude(cal.gregorian_to_jd(2024, 3, 20, 3)) + 180) % 360) - 180) < 3)

# --- eight palaces & najia -------------------------------------------------
check("all 64 have a palace", len(liuyao.PALACE) == 64)
check("大有 #14 in Qian palace", liuyao.PALACE[14][0] == 0)
check("比 #8 归魂 pos7", liuyao.PALACE[8][1] == 7)
qian_lines = liuyao._line_branches(bagua.Hexagram((1, 1, 1, 1, 1, 1)))
check("Qian najia 子寅辰午申戌", qian_lines == [0, 2, 4, 6, 8, 10])

# --- methods run end to end ------------------------------------------------
rng = random.Random(42)
r = yijing.cast("coin", rng)
check("coin cast has 6 lines", len(r["values"]) == 6)
check("coin values in 6..9", all(v in (6, 7, 8, 9) for v in r["values"]))
r2 = yijing.cast("yarrow", random.Random(1))
check("yarrow values in 6..9", all(v in (6, 7, 8, 9) for v in r2["values"]))
m = meihua.from_numbers(5, 8)
check("meihua builds hexagram", 1 <= m["primary"].number <= 64)
check("meihua has verdict", isinstance(m["verdict"], str))
mt = meihua.from_time(2024, 2, 10, 14)
check("meihua time has lunar", mt["lunar"]["month"] == 1)
lo = liuyao.cast(2024, 2, 10, 14, random.Random(7))
check("liuyao overlay 6 lines", len(lo["overlay"]["lines"]) == 6)
check("liuyao world in 1..6", 1 <= lo["overlay"]["world"] <= 6)

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
