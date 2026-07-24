"""Mei Hua Yi Shu 梅花易數 — Plum Blossom Numerology.

Deterministic: the *input* is the oracle, not chance. A hexagram is built from
two numbers (or from the moment's lunar date), and the moving line splits the
figure into a 體 (host / self) trigram and a 用 (use / situation) trigram. The
element relation between them is the core reading, which we can give in full.

Xiantian (Fu Xi) trigram numbers: 1 Qian, 2 Dui, 3 Li, 4 Zhen,
5 Xun, 6 Kan, 7 Gen, 8 Kun  (== core.bagua.TRIGRAMS index + 1).
"""

from core import bagua, wuxing, calendar_cn as cal, ganzhi


def _trigram_bits(xiantian_number):
    """Xiantian number 1..8 (0 treated as 8) -> trigram bits."""
    n = xiantian_number % 8
    if n == 0:
        n = 8
    return bagua.TRIGRAMS[n - 1][4]


def build(upper_num, lower_num, moving_total):
    """Assemble a Plum Blossom reading from the three derived numbers.
    upper_num -> outer/upper trigram, lower_num -> inner/lower trigram,
    moving line = moving_total mod 6 (0 -> 6), counted from the bottom."""
    upper_bits = _trigram_bits(upper_num)
    lower_bits = _trigram_bits(lower_num)
    bits = tuple(lower_bits) + tuple(upper_bits)
    line = moving_total % 6
    if line == 0:
        line = 6

    primary = bagua.Hexagram(bits)
    # transform the moving line
    tb = list(bits)
    tb[line - 1] = 1 - tb[line - 1]
    changed = bagua.Hexagram(tuple(tb))

    # host/use: the trigram CONTAINING the moving line is 用 (use), other is 體.
    moving_in_lower = line <= 3
    lower_el = bagua.TRIGRAMS[bagua.trigram_index(lower_bits)][5]
    upper_el = bagua.TRIGRAMS[bagua.trigram_index(upper_bits)][5]
    if moving_in_lower:
        use_el, host_el = lower_el, upper_el
        host_pos, use_pos = "upper", "lower"
    else:
        use_el, host_el = upper_el, lower_el
        host_pos, use_pos = "lower", "upper"

    rel = wuxing.relation(host_el, use_el)
    verdict = {
        "same":         "Host and Use share an element — steady, evenly matched.",
        "generates_me": "Use generates Host — outside forces nourish you. Favorable.",
        "i_overcome":   "Host overcomes Use — you command the situation. Favorable.",
        "i_generate":   "Host generates Use — you spend yourself outward. Draining.",
        "overcomes_me": "Use overcomes Host — the situation presses on you. Adverse.",
    }[rel]

    return {
        "method": "meihua",
        "primary": primary,
        "changed": changed,
        "moving": [line],
        "host": {"pos": host_pos, "element": host_el},
        "use": {"pos": use_pos, "element": use_el},
        "relation": rel,
        "verdict": verdict,
    }


def from_numbers(a, b):
    """Two observed numbers -> reading. a sets the upper trigram, b the lower;
    their sum sets the moving line."""
    return build(a, b, a + b)


def from_time(year, month, day, hour):
    """The moment's lunar date -> reading (the classic time method).

    upper = (year-branch no. + lunar month + lunar day)
    lower = upper + hour-branch no.
    moving line = lower total mod 6.
    Branch numbers are 1-based zodiac ordinals (子=1 ... 亥=12)."""
    lun = cal.lunar_date(year, month, day)
    year_branch_no = ((lun["year"] - 4) % 12) + 1
    hour_branch_no = ganzhi.hour_branch_of(hour) + 1

    upper_total = year_branch_no + lun["month"] + lun["day"]
    lower_total = upper_total + hour_branch_no
    reading = build(upper_total, lower_total, lower_total)
    reading["lunar"] = lun
    reading["inputs"] = {
        "year_branch_no": year_branch_no,
        "lunar_month": lun["month"],
        "lunar_day": lun["day"],
        "hour_branch_no": hour_branch_no,
    }
    return reading
