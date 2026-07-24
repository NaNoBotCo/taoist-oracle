"""Bazi 八字 / Four Pillars of Destiny — the deterministic birth chart.

A birth moment resolves to four Ganzhi pillars (year, month, day, hour), already
computed by the spine (core.ganzhi.four_pillars, solar-term bounded as Bazi
requires). On top of that this module lays the fixed scaffolding every Bazi
reading uses:

    - the Day Master (日主): the day pillar's stem — the chart's "self"
    - hidden stems (藏干): the 1-3 stems each Earthly Branch carries
    - the Ten Gods (十神): every other stem's relation to the Day Master
    - nayin (納音): each pillar's "sound element"
    - the five-element tally across the eight characters
    - the luck pillars (大運): the 10-year decade cycles

All of the above is exact, rule-based computation. The DAY-MASTER STRENGTH read
is a labelled heuristic — real strength assessment (身強/身弱 and the 用神) is a
whole interpretive craft; here we give the supporting-vs-draining balance and say
so, rather than pronounce a verdict.
"""

from core import ganzhi, wuxing
from core import calendar_cn as cal

# --- Hidden stems 藏干: stem indices each branch carries, principal (本氣) first ---
HIDDEN_STEMS = {
    0:  [9],            # 子  癸
    1:  [5, 9, 7],      # 丑  己 癸 辛
    2:  [0, 2, 4],      # 寅  甲 丙 戊
    3:  [1],            # 卯  乙
    4:  [4, 1, 9],      # 辰  戊 乙 癸
    5:  [2, 6, 4],      # 巳  丙 庚 戊
    6:  [3, 5],         # 午  丁 己
    7:  [5, 3, 1],      # 未  己 丁 乙
    8:  [6, 8, 4],      # 申  庚 壬 戊
    9:  [7],            # 酉  辛
    10: [4, 7, 3],      # 戌  戊 辛 丁
    11: [8, 0],         # 亥  壬 甲
}

# --- Ten Gods 十神: (relation-to-DM, same-polarity?) -> (zh, en) -------------
TEN_GODS = {
    ("same", True):          ("比肩", "Peer"),
    ("same", False):         ("劫財", "Rob Wealth"),
    ("i_generate", True):    ("食神", "Eating God"),
    ("i_generate", False):   ("傷官", "Hurting Officer"),
    ("i_overcome", True):    ("偏財", "Indirect Wealth"),
    ("i_overcome", False):   ("正財", "Direct Wealth"),
    ("overcomes_me", True):  ("七殺", "Seven Killings"),
    ("overcomes_me", False): ("正官", "Direct Officer"),
    ("generates_me", True):  ("偏印", "Indirect Resource"),
    ("generates_me", False): ("正印", "Direct Resource"),
}


def ten_god(dm_stem, other_stem):
    rel = wuxing.relation(ganzhi.STEM_ELEMENT[dm_stem], ganzhi.STEM_ELEMENT[other_stem])
    same_pol = (dm_stem % 2) == (other_stem % 2)
    return TEN_GODS[(rel, same_pol)]


# --- Nayin 納音: 30 entries, one per two consecutive sexagenary indices -------
NAYIN = [
    ("海中金", "Metal in the Sea"), ("爐中火", "Fire in the Furnace"),
    ("大林木", "Wood of the Great Forest"), ("路旁土", "Earth by the Roadside"),
    ("劍鋒金", "Metal of the Sword's Edge"), ("山頭火", "Fire on the Mountain Peak"),
    ("澗下水", "Water in the Ravine"), ("城頭土", "Earth of the City Wall"),
    ("白鑞金", "White Wax Metal"), ("楊柳木", "Willow Wood"),
    ("泉中水", "Water of the Spring"), ("屋上土", "Earth on the Rooftop"),
    ("霹靂火", "Thunderbolt Fire"), ("松柏木", "Pine and Cypress Wood"),
    ("長流水", "Long-Flowing Water"), ("沙中金", "Metal in the Sand"),
    ("山下火", "Fire at the Foot of the Hill"), ("平地木", "Wood of the Level Ground"),
    ("壁上土", "Earth on the Wall"), ("金箔金", "Gold-Foil Metal"),
    ("覆燈火", "Sheltered Lamp Fire"), ("天河水", "Water of the Milky Way"),
    ("大驛土", "Earth of the Great Post-Road"), ("釵釧金", "Metal of Hairpin and Bracelet"),
    ("桑柘木", "Mulberry Wood"), ("大溪水", "Water of the Great Stream"),
    ("沙中土", "Earth in the Sand"), ("天上火", "Fire in the Heavens"),
    ("石榴木", "Pomegranate Wood"), ("大海水", "Water of the Great Ocean"),
]


def nayin(index):
    return NAYIN[(index % 60) // 2]


# --------------------------------------------------------------------------
# the chart
# --------------------------------------------------------------------------
def _pillar_view(pillar, dm_stem, is_day=False):
    """Everything shown for one pillar. The day pillar's stem is the Day Master
    itself, so it carries no Ten God — it is the reference, not a relation."""
    hidden = HIDDEN_STEMS[pillar.branch]
    return {
        "stem": pillar.stem,
        "branch": pillar.branch,
        "stem_zh": ganzhi.STEMS[pillar.stem][0],
        "branch_zh": ganzhi.BRANCHES[pillar.branch][0],
        "name_zh": pillar.name("zh"),
        "animal": pillar.animal(),
        "stem_element": ganzhi.STEM_ELEMENT[pillar.stem],
        "branch_element": ganzhi.BRANCH_ELEMENT[pillar.branch],
        "stem_god": None if is_day else ten_god(dm_stem, pillar.stem),
        "hidden": [{"stem": s, "zh": ganzhi.STEMS[s][0],
                    "element": ganzhi.STEM_ELEMENT[s],
                    "god": ten_god(dm_stem, s)} for s in hidden],
        "nayin": nayin(pillar.index),
    }


def element_tally(pillars):
    """Count the five elements across the eight characters: four stems, plus each
    branch's PRINCIPAL hidden stem (its 本氣). Returns {element: count}."""
    tally = {e: 0 for e in range(5)}
    for p in pillars.values():
        tally[ganzhi.STEM_ELEMENT[p.stem]] += 1
        tally[ganzhi.STEM_ELEMENT[HIDDEN_STEMS[p.branch][0]]] += 1
    return tally


def strength_heuristic(pillars):
    """A LABELLED heuristic, not a verdict. Supporters of the Day Master are the
    same element (比劫) and the element that generates it (印); drainers are what
    it produces (食傷), controls (財) and what controls it (官殺). We also note
    whether the birth month supports the Day Master. Returns a dict."""
    dm = pillars["day"].stem
    dm_el = ganzhi.STEM_ELEMENT[dm]
    support, drain = 0, 0
    # weigh the eight characters by their relation to the Day Master
    chars = []
    for key, p in pillars.items():
        chars.append(p.stem)
        chars.append(HIDDEN_STEMS[p.branch][0])
    for s in chars:
        rel = wuxing.relation(dm_el, ganzhi.STEM_ELEMENT[s])
        if rel in ("same", "generates_me"):
            support += 1
        else:
            drain += 1
    month_el = ganzhi.STEM_ELEMENT[HIDDEN_STEMS[pillars["month"].branch][0]]
    month_rel = wuxing.relation(dm_el, month_el)
    seasoned = month_rel in ("same", "generates_me")
    if support > drain and seasoned:
        label = "leans strong"
    elif drain > support and not seasoned:
        label = "leans weak"
    else:
        label = "mixed / balanced"
    return {"support": support, "drain": drain, "month_supports": seasoned,
            "label": label}


def _jie_jd(jd, forward):
    """JD of the bounding 節 (jie / month-start solar term) — the next one if
    forward, the previous one if backward. Jie sit at ecliptic longitudes
    15, 45, ... 345 (every 30 deg, offset 15)."""
    import math
    lon = cal.solar_longitude(jd)
    if forward:
        k = math.floor((lon - 15) / 30) + 1
    else:
        k = math.ceil((lon - 15) / 30) - 1
    target = (15 + 30 * k) % 360
    diff = ((target - lon + 180) % 360 - 180)
    approx = jd + diff / 0.98565
    return cal.solar_term_jd(target, approx)


def luck_pillars(year, month, day, hour, gender, count=8):
    """The 大運 decade-luck pillars. Direction follows the classical rule
    (阳男阴女順, 阴男阳女逆): forward if the year stem is yang and the person is
    male, or the year stem is yin and female; backward otherwise. The start age
    is the distance to the bounding 節, three days to the year.

    gender: 'male' or 'female' (the traditional rule keys off birth sex; the
    chart itself does not need it). Returns None if gender is not given."""
    if gender not in ("male", "female"):
        return None
    yp = ganzhi.year_pillar(year, month, day)
    year_yang = (yp.stem % 2 == 0)
    forward = (year_yang and gender == "male") or (not year_yang and gender == "female")

    birth_jd = cal.gregorian_to_jd(year, month, day, hour)
    jie = _jie_jd(birth_jd, forward)
    days = abs(jie - birth_jd)
    start_years = days / 3.0
    start_y = int(start_years)
    start_m = int(round((start_years - start_y) * 12))
    if start_m == 12:
        start_y, start_m = start_y + 1, 0

    mp = ganzhi.month_pillar(year, month, day, hour)
    step = 1 if forward else -1
    out = []
    for i in range(count):
        idx = (mp.index + step * (i + 1)) % 60
        p = ganzhi.Pillar(idx)
        age = start_y + 10 * i
        out.append({
            "index": idx, "name_zh": p.name("zh"), "animal": p.animal(),
            "stem_element": ganzhi.STEM_ELEMENT[p.stem],
            "start_age": age,
        })
    return {"forward": forward, "start_age_years": start_y, "start_age_months": start_m,
            "pillars": out}


def chart(year, month, day, hour, gender=None):
    """The full Bazi chart for a birth moment."""
    pillars = ganzhi.four_pillars(year, month, day, hour)
    dm = pillars["day"].stem
    order = ["year", "month", "day", "hour"]
    views = {k: _pillar_view(pillars[k], dm, is_day=(k == "day")) for k in order}
    return {
        "input": {"year": year, "month": month, "day": day, "hour": hour,
                  "gender": gender},
        "order": order,
        "pillars": views,
        "day_master": {
            "stem": dm, "zh": ganzhi.STEMS[dm][0],
            "element": ganzhi.STEM_ELEMENT[dm],
            "polarity": "yang" if dm % 2 == 0 else "yin",
        },
        "elements": element_tally(pillars),
        "strength": strength_heuristic(pillars),
        "luck": luck_pillars(year, month, day, hour, gender),
    }
