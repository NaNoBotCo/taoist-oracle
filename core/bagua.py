"""Ba Gua 八卦 spine: the 8 trigrams, the 64 hexagrams, and hexagram operations.

Lines are represented bottom-to-top. A *cast* line carries one of the four
classical values:
    6  old yin   (⚋ moving -> becomes yang)
    7  young yang (⚊ stable)
    8  young yin  (⚋ stable)
    9  old yang   (⚊ moving -> becomes yin)

yang = 7 or 9, yin = 6 or 8, moving = 6 or 9.
"""

from data import hexagrams
from core import wuxing

# Trigram table, indexed 0..7. bits are (bottom, middle, top), 1=yang 0=yin.
# element uses core.wuxing constants.
TRIGRAMS = [
    #  hanzi pinyin  english      symbol bits          element
    ("乾", "Qián", "Heaven",   "☰", (1, 1, 1), wuxing.METAL),
    ("兌", "Duì",  "Lake",     "☱", (1, 1, 0), wuxing.METAL),
    ("離", "Lí",   "Fire",     "☲", (1, 0, 1), wuxing.FIRE),
    ("震", "Zhèn", "Thunder",  "☳", (1, 0, 0), wuxing.WOOD),
    ("巽", "Xùn",  "Wind",     "☴", (0, 1, 1), wuxing.WOOD),
    ("坎", "Kǎn",  "Water",    "☵", (0, 1, 0), wuxing.WATER),
    ("艮", "Gèn",  "Mountain", "☶", (0, 0, 1), wuxing.EARTH),
    ("坤", "Kūn",  "Earth",    "☷", (0, 0, 0), wuxing.EARTH),
]

_BITS_TO_TRIGRAM = {t[4]: i for i, t in enumerate(TRIGRAMS)}


def is_yang(value):
    return value in (7, 9)


def is_moving(value):
    return value in (6, 9)


def line_glyph(value, moving_mark=True):
    """A single-line glyph for display. value may be a cast value (6-9) or a
    plain bit (1 yang / 0 yin)."""
    if value in (1, 0):
        yang, moving = bool(value), False
    else:
        yang, moving = is_yang(value), is_moving(value)
    body = "▅▅▅▅▅▅▅" if yang else "▅▅▅   ▅▅▅"
    if moving_mark and moving:
        return body + ("  →○" if yang else "  →×")   # old yang / old yin
    return body


def bits_of(values):
    """Present-state bits (1/0) bottom-to-top from cast values or bits."""
    return tuple(1 if (v in (1, 7, 9)) else 0 for v in values)


def transform_bits(values):
    """Bits after moving lines flip. Non-moving lines keep their state."""
    out = []
    for v in values:
        if v == 6:      # old yin -> yang
            out.append(1)
        elif v == 9:    # old yang -> yin
            out.append(0)
        else:
            out.append(1 if v in (1, 7) else 0)
    return tuple(out)


def trigram_index(bits3):
    return _BITS_TO_TRIGRAM[tuple(bits3)]


def hexagram_number(bits6):
    lower = trigram_index(bits6[0:3])
    upper = trigram_index(bits6[3:6])
    return hexagrams.BY_TRIGRAMS[(lower, upper)]


class Hexagram:
    """A resolved hexagram: its King Wen identity plus its trigrams."""

    def __init__(self, bits6):
        self.bits = tuple(bits6)
        self.number = hexagram_number(self.bits)
        row = hexagrams.BY_NUMBER[self.number]
        self.hanzi = row[1]
        self.pinyin = row[2]
        self.english = row[3]
        self.lower = row[4]
        self.upper = row[5]
        self.gloss = row[6]

    @property
    def palace_element(self):
        """The element of the upper (outer) trigram — used as the hexagram's
        own element for six-relatives assignment. (A simplification of full
        palace theory, sufficient for the spine.)"""
        return TRIGRAMS[self.upper][5]

    def label(self):
        return f"#{self.number} {self.hanzi} {self.pinyin} — {self.english}"

    def __repr__(self):
        return f"<Hexagram {self.label()}>"


def moving_positions(values):
    """1-indexed positions (bottom=1) of moving lines."""
    return [i + 1 for i, v in enumerate(values) if is_moving(v)]
