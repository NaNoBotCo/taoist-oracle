"""The 64 hexagrams in King Wen order.

Each row: (number, hanzi, pinyin, english, lower_trigram_idx, upper_trigram_idx, gloss)

Trigram indices follow core.bagua.TRIGRAMS:
    0 Qian  1 Dui  2 Li  3 Zhen  4 Xun  5 Kan  6 Gen  7 Kun

The gloss is an original, concise reading (interpretive, not a translation of
any single source). The full 384 line-texts are a separate corpus and live in
LINE_TEXTS below, which starts seeded and is meant to be extended.
"""

KINGWEN = [
    (1,  "乾", "Qián",      "The Creative",            0, 0, "Pure initiating force; sustained, upright action succeeds."),
    (2,  "坤", "Kūn",       "The Receptive",           7, 7, "Yielding devotion; carry, nourish, follow rather than lead."),
    (3,  "屯", "Zhūn",      "Difficulty at the Beginning", 3, 5, "A hard sprouting; find helpers, do not force the first move."),
    (4,  "蒙", "Méng",      "Youthful Folly",          5, 6, "Inexperience seeking a teacher; answer the sincere question once."),
    (5,  "需", "Xū",        "Waiting",                 0, 5, "Danger ahead; nourish yourself and wait with confidence."),
    (6,  "訟", "Sòng",      "Conflict",                5, 0, "Dispute you cannot win outright; seek mediation, do not push to the end."),
    (7,  "師", "Shī",       "The Army",                5, 7, "Discipline under one trusted leader; a just cause moves the mass."),
    (8,  "比", "Bǐ",        "Holding Together",        7, 5, "Union around a center; join early and sincerely or be left out."),
    (9,  "小畜", "Xiǎo Xù", "Small Taming",            0, 4, "Gentle restraint of strength; small means, patient accumulation."),
    (10, "履", "Lǚ",        "Treading",                1, 0, "Walking on the tiger's tail; correct conduct disarms danger."),
    (11, "泰", "Tài",       "Peace",                   0, 7, "Heaven and earth mingle; flourishing, but tend the turning point."),
    (12, "否", "Pǐ",        "Standstill",              7, 0, "Powers drift apart; withdraw, keep integrity, wait out the block."),
    (13, "同人", "Tóng Rén","Fellowship",              2, 0, "Open community with all; shared aims in the light succeed."),
    (14, "大有", "Dà Yǒu",  "Great Possession",        0, 2, "Abundance clearly held; be modest and generous with plenty."),
    (15, "謙", "Qiān",      "Modesty",                 6, 7, "Height that stays low; modesty carries every undertaking through."),
    (16, "豫", "Yù",        "Enthusiasm",              7, 3, "Readiness that moves others; align with the time, rouse gladly."),
    (17, "隨", "Suí",       "Following",               3, 1, "Adapt and follow; lead by yielding to what is right now."),
    (18, "蠱", "Gǔ",        "Work on the Decayed",     4, 6, "Repair what was spoiled; face the rot, then rebuild carefully."),
    (19, "臨", "Lín",       "Approach",                1, 7, "Something great draws near; act while the season favors growth."),
    (20, "觀", "Guān",      "Contemplation",           7, 4, "Observe from height; be the example that others take their bearings by."),
    (21, "噬嗑", "Shì Kè",  "Biting Through",          3, 2, "An obstacle in the bite; act decisively, apply just correction."),
    (22, "賁", "Bì",        "Grace",                   2, 6, "Beauty and form; adornment helps in small things, not the essential."),
    (23, "剝", "Bō",        "Splitting Apart",         7, 6, "The structure erodes from below; do not act, preserve the seed."),
    (24, "復", "Fù",        "Return",                  3, 7, "The light returns; a turning point, movement resumes gently."),
    (25, "無妄", "Wú Wàng", "Innocence",               3, 0, "Act from the unspoiled instinct; the unexpected tests sincerity."),
    (26, "大畜", "Dà Xù",   "Great Taming",            0, 6, "Great force held and stored; discipline builds real power."),
    (27, "頤", "Yí",        "Nourishment",             3, 6, "Watch what you take in and give out; feed the right things."),
    (28, "大過", "Dà Guò",  "Great Exceeding",         4, 1, "The beam sags under load; extraordinary times, act while you can."),
    (29, "坎", "Kǎn",       "The Abysmal Water",       5, 5, "Repeated danger; stay sincere, flow through, do not lose the center."),
    (30, "離", "Lí",        "The Clinging Fire",       2, 2, "Radiance that depends on its fuel; clarity through what you cleave to."),
    (31, "咸", "Xián",      "Influence",               6, 1, "Mutual attraction; keep the heart open and receptive to move another."),
    (32, "恆", "Héng",      "Duration",                4, 3, "Enduring constancy; hold your course, renew without changing aim."),
    (33, "遯", "Dùn",       "Retreat",                 6, 0, "Timely withdrawal; retreat is strength when the small advances."),
    (34, "大壯", "Dà Zhuàng","Great Power",            0, 3, "Great vigor; power is safe only when joined to what is right."),
    (35, "晉", "Jìn",       "Progress",                7, 2, "Easy rising like the sun; advance in the open, be recognized."),
    (36, "明夷", "Míng Yí", "Darkening of the Light",  2, 7, "The light is wounded; veil your brilliance, endure the dark time."),
    (37, "家人", "Jiā Rén", "The Family",              2, 4, "Order within the house; each keeps their place, warmth with limits."),
    (38, "睽", "Kuí",       "Opposition",              1, 2, "Estrangement and misreading; small accord is possible, not the large."),
    (39, "蹇", "Jiǎn",      "Obstruction",             6, 5, "An obstacle you cannot pass alone; turn inward, seek allies."),
    (40, "解", "Xiè",       "Deliverance",             5, 3, "The knot loosens; resolve tension, forgive, return to the ordinary."),
    (41, "損", "Sǔn",       "Decrease",                1, 6, "Decrease below to serve above; sincere reduction brings gain."),
    (42, "益", "Yì",        "Increase",                3, 4, "Decrease above to enrich below; a favorable time for great deeds."),
    (43, "夬", "Guài",      "Breakthrough",            0, 1, "Resolute breakthrough; name the wrong openly, not by force alone."),
    (44, "姤", "Gòu",       "Coming to Meet",          4, 0, "An unbidden meeting; a small dark thing enters, do not let it spread."),
    (45, "萃", "Cuì",       "Gathering Together",      7, 1, "Gathering around a center; assemble with a clear focal purpose."),
    (46, "升", "Shēng",     "Pushing Upward",          4, 7, "Effortful ascent; grow step by step, seek the one who can help."),
    (47, "困", "Kùn",       "Oppression",              5, 1, "Exhaustion and confinement; keep faith inwardly, say little."),
    (48, "井", "Jǐng",      "The Well",                4, 5, "The constant source; the well does not move, tend it and it feeds all."),
    (49, "革", "Gé",        "Revolution",              2, 1, "Radical change at the right moment; molt only when trust is ready."),
    (50, "鼎", "Dǐng",      "The Cauldron",            4, 2, "Transforming and nourishing; refine the raw into the offered."),
    (51, "震", "Zhèn",      "The Arousing Thunder",    3, 3, "Shock that startles then passes; keep composure, laughter follows."),
    (52, "艮", "Gèn",       "Keeping Still Mountain",  6, 6, "Stillness at the right time; quiet the mind, act only when moved."),
    (53, "漸", "Jiàn",      "Development",             6, 4, "Gradual, orderly progress; advance like a tree, no skipped stages."),
    (54, "歸妹", "Guī Mèi", "The Marrying Maiden",     1, 3, "Entering a subordinate bond; know your place, keep the long view."),
    (55, "豐", "Fēng",      "Abundance",               2, 3, "A peak of fullness; be like the noon sun, use the bright hour well."),
    (56, "旅", "Lǚ",        "The Wanderer",            6, 2, "A stranger in transit; stay modest and correct, hold few things."),
    (57, "巽", "Xùn",       "The Gentle Wind",         4, 4, "Penetrating influence; gentle persistence reaches where force cannot."),
    (58, "兌", "Duì",       "The Joyous Lake",         1, 1, "Open gladness; true joy is shared and honest, not flattery."),
    (59, "渙", "Huàn",      "Dispersion",              5, 4, "Dissolving rigidity; scatter what blocks, reunite around a purpose."),
    (60, "節", "Jié",       "Limitation",              1, 5, "Wholesome limits; set measures, but do not make them galling."),
    (61, "中孚", "Zhōng Fú","Inner Truth",             1, 4, "Sincerity at the center; inner truth moves even the distant and dumb."),
    (62, "小過", "Xiǎo Guò","Small Exceeding",         6, 3, "Exceed only in small things; stay low, the bird should not fly high."),
    (63, "既濟", "Jì Jì",   "After Completion",        2, 5, "The task is done; order achieved decays, guard against the slack."),
    (64, "未濟", "Wèi Jì",  "Before Completion",       5, 2, "Almost there; the crossing is not finished, place each step with care."),
]

# number -> row, and (lower, upper) -> number
BY_NUMBER = {row[0]: row for row in KINGWEN}
BY_TRIGRAMS = {(row[4], row[5]): row[0] for row in KINGWEN}

# Extensible line-text corpus. Key: (hexagram_number, line_position 1..6).
# Seeded empty on purpose — the mechanics below never depend on it; interpretation
# text is a data layer to grow. Fill entries as {(1,1): "Nine at the beginning: ..."}.
LINE_TEXTS = {}
