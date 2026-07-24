"""Wu Xing 五行 — the Five Elements and their two cycles.

A tiny relational engine reused by every method: trigram elements, branch/stem
elements, and the generating (生 shēng) and overcoming (剋 kè) relations that
Liu Yao and the deterministic systems read strengths from.
"""

# Canonical order Wood, Fire, Earth, Metal, Water
WOOD, FIRE, EARTH, METAL, WATER = range(5)

NAMES = {
    WOOD:  ("木", "Wood"),
    FIRE:  ("火", "Fire"),
    EARTH: ("土", "Earth"),
    METAL: ("金", "Metal"),
    WATER: ("水", "Water"),
}

# generating cycle: each element produces the next
_SHENG_NEXT = {WOOD: FIRE, FIRE: EARTH, EARTH: METAL, METAL: WATER, WATER: WOOD}
# overcoming cycle: each element controls another
_KE_TARGET = {WOOD: EARTH, EARTH: WATER, WATER: FIRE, FIRE: METAL, METAL: WOOD}


def name(e, lang="en"):
    hanzi, en = NAMES[e]
    return hanzi if lang == "zh" else en


def generates(a, b):
    """True if a produces b (a 生 b)."""
    return _SHENG_NEXT[a] == b


def overcomes(a, b):
    """True if a controls b (a 剋 b)."""
    return _KE_TARGET[a] == b


def relation(subject, other):
    """How `other` stands to `subject`, in the Liu Yao 'six relatives' sense.

    Returns one of: 'same', 'generates_me', 'i_generate', 'overcomes_me',
    'i_overcome'.
    """
    if subject == other:
        return "same"
    if _SHENG_NEXT[other] == subject:
        return "generates_me"     # resource / parent  (印/父母)
    if _SHENG_NEXT[subject] == other:
        return "i_generate"       # output / offspring (子孫)
    if _KE_TARGET[other] == subject:
        return "overcomes_me"     # authority / officer (官鬼)
    if _KE_TARGET[subject] == other:
        return "i_overcome"       # what I control / wealth (妻財)
    raise ValueError("unreachable")


# The Liu Yao "six relatives" label for a relation, relative to the hexagram's
# own palace element (the 'self' = 兄弟 siblings).
SIX_RELATIVES = {
    "same":         ("兄弟", "Siblings"),
    "generates_me": ("父母", "Parent"),
    "i_generate":   ("子孫", "Offspring"),
    "overcomes_me": ("官鬼", "Officer/Ghost"),
    "i_overcome":   ("妻財", "Wealth"),
}
