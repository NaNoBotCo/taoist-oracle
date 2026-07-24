#!/usr/bin/env python3
"""Taoist Oracle — a single engine for the cast-oracle divination methods.

Numbered-menu console. Everything runs offline, pure standard library.

    python3 oracle.py
"""

import random
import sys
from datetime import datetime

from core import bagua, wuxing, ganzhi
from methods import yijing, meihua, liuyao

LINE = "─" * 60


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def _trigram_name(idx):
    t = bagua.TRIGRAMS[idx]
    return f"{t[3]} {t[0]} {t[1]} ({t[2]})"


def draw_hexagram(hexagram, cast_values=None, title=""):
    """Draw a hexagram top-to-bottom with big line glyphs. If cast_values is
    given, moving lines are marked."""
    out = []
    if title:
        out.append(title)
    # lines are stored bottom(1)..top(6); print top first
    for pos in range(6, 0, -1):
        if cast_values is not None:
            glyph = bagua.line_glyph(cast_values[pos - 1])
        else:
            glyph = bagua.line_glyph(hexagram.bits[pos - 1])
        out.append(f"   {glyph}")
    out.append("")
    out.append(f"   {hexagram.label()}")
    out.append(f"   upper: {_trigram_name(hexagram.upper)}")
    out.append(f"   lower: {_trigram_name(hexagram.lower)}")
    out.append(f"   {hexagram.gloss}")
    return "\n".join(out)


def show_yijing(reading):
    print(LINE)
    label = "yarrow stalks" if reading["method"] == "yarrow" else "three coins"
    print(f"YIJING 易經  —  cast by {label}\n")
    print(draw_hexagram(reading["primary"], reading["values"],
                        title="Present hexagram:"))
    if reading["moving"]:
        pos = ", ".join(str(p) for p in reading["moving"])
        print(f"\n   Moving line(s): {pos}  (counted from the bottom)")
        print()
        print(draw_hexagram(reading["changed"], title="Changes into:"))
        print("\n   Read the present hexagram for the situation now, the moving")
        print("   lines for the pivot, and the changed hexagram for where it tends.")
    else:
        print("\n   No moving lines — a still answer. Read the hexagram as it stands.")
    print(LINE)


def show_meihua(reading):
    print(LINE)
    print("MEI HUA YI SHU 梅花易數  —  Plum Blossom\n")
    if "lunar" in reading:
        lun = reading["lunar"]
        leap = "leap " if lun["is_leap"] else ""
        print(f"   Moment -> lunar {lun['year']}, {leap}month {lun['month']}, day {lun['day']}")
        i = reading["inputs"]
        print(f"   numbers: year-branch {i['year_branch_no']} + month {i['lunar_month']}"
              f" + day {i['lunar_day']} (+ hour {i['hour_branch_no']})\n")
    print(draw_hexagram(reading["primary"], title="Hexagram:"))
    print(f"\n   Moving line: {reading['moving'][0]}")
    print(draw_hexagram(reading["changed"], title="\nChanges into:"))
    host, use = reading["host"], reading["use"]
    print(f"\n   體 Host (self):     {use_el_name(host['element'])}  [{host['pos']} trigram]")
    print(f"   用 Use (situation): {use_el_name(use['element'])}  [{use['pos']} trigram]")
    print(f"\n   {reading['verdict']}")
    print(LINE)


def use_el_name(e):
    hz, en = wuxing.NAMES[e]
    return f"{hz} {en}"


def show_liuyao(reading, when):
    print(LINE)
    print(f"WEN WANG GUA 文王卦 / LIU YAO 六爻  —  {when}\n")
    _liuyao_sheet(reading["primary"], reading["values"], reading["overlay"],
                  "Present hexagram")
    if reading["changed"]:
        print()
        _liuyao_sheet(reading["changed"], None, reading["overlay_changed"],
                      "Changed hexagram", moving=reading["moving"], show_marks=False)
    ov = reading["overlay"]
    print(f"\n   Day pillar: {ov['day_pillar'].name('zh')} ({ov['day_pillar'].name('en')})")
    print(f"   Void (旬空) today: {' '.join(ov['void_branches'])}")
    print(f"   Palace: {ov['palace'][0]} {ov['palace'][1]} — element "
          f"{use_el_name(ov['palace_element'])}")
    print(f"   世 World line: {ov['world']}   應 Response line: {ov['response']}")
    print(LINE)


def _liuyao_sheet(hexagram, cast_values, overlay, title, moving=None, show_marks=True):
    print(f"{title}: {hexagram.label()}")
    lines = {l["pos"]: l for l in overlay["lines"]}
    for pos in range(6, 0, -1):
        l = lines[pos]
        if cast_values is not None:
            glyph = bagua.line_glyph(cast_values[pos - 1])
        else:
            glyph = bagua.line_glyph(hexagram.bits[pos - 1])
            if moving and pos in moving:
                glyph += " *"
        marks = []
        if show_marks and l["world"]:
            marks.append("世")
        if show_marks and l["response"]:
            marks.append("應")
        mark = "".join(marks) or "  "
        rel = l["relative"][0]
        void = "空" if l["void"] else " "
        beast = l["beast"]
        branch = l["branch_name"] + use_el_name(l["element"]).split()[0]
        print(f"   {mark:2} {beast} {rel} {branch}{void}  {glyph}")


# --------------------------------------------------------------------------
# menu actions
# --------------------------------------------------------------------------
def ask_int(prompt):
    while True:
        raw = input(prompt).strip()
        if raw.lstrip("-").isdigit():
            return int(raw)
        print("   Please enter a number.")


def act_yijing(method):
    input(f"\n   Focus your question, then press Enter to cast ({method})... ")
    show_yijing(yijing.cast(method))


def act_meihua_numbers():
    a = ask_int("\n   First number (sets the upper trigram): ")
    b = ask_int("   Second number (sets the lower trigram): ")
    show_meihua(meihua.from_numbers(a, b))


def act_meihua_time():
    now = datetime.now()
    show_meihua(meihua.from_time(now.year, now.month, now.day, now.hour))


def act_liuyao():
    now = datetime.now()
    input("\n   Focus your question, then press Enter to cast... ")
    reading = liuyao.cast(now.year, now.month, now.day, now.hour)
    show_liuyao(reading, now.strftime("%Y-%m-%d %H:%M"))


def show_odds():
    print(LINE)
    print("THE ODDS — three coins vs. yarrow stalks\n")
    print(f"   {'line':<20}{'yarrow':>10}{'coins':>10}")
    print(f"   {'-'*40}")
    for value, zh, en, yar, coin in yijing.odds_table():
        label = f"{value} {zh} {en}"
        print(f"   {label:<20}{yar:>9.2f}%{coin:>9.2f}%")
    print(f"   {'-'*40}")
    print("\n   What stays the same under BOTH methods:")
    print("     • each line is 50% yin, 50% yang")
    print("     • any line is moving (changing) exactly 25% of the time")
    print("\n   What the coin method changes — only the internal lean:")
    print("     • Yarrow leans toward stable young-yin (少陰, its commonest")
    print("       line) and, among moving lines, toward old-yang over old-yin")
    print("       by 3 to 1 — a built-in tilt toward yang giving way to yin.")
    print("     • Coins flatten that to perfect symmetry: old yin and old yang")
    print("       become equally likely. Same amount of change, no direction.")
    print(LINE)


MENU = [
    ("I Ching — cast with three coins", lambda: act_yijing("coin")),
    ("I Ching — cast with yarrow stalks", lambda: act_yijing("yarrow")),
    ("Plum Blossom — from two numbers", act_meihua_numbers),
    ("Plum Blossom — from this moment", act_meihua_time),
    ("Wen Wang Gua (Liu Yao) — cast for now", act_liuyao),
    ("The odds — coins vs. yarrow (statistics)", show_odds),
]


def main():
    print("\n  ☯  TAOIST ORACLE  —  cast-oracle methods on one engine\n")
    while True:
        print()
        for i, (label, _) in enumerate(MENU, 1):
            print(f"   {i}. {label}")
        print("   0. Quit")
        choice = input("\n   Choose: ").strip()
        if choice in ("0", "q", "quit", "exit"):
            print("\n  ☯  Farewell.\n")
            return
        if choice.isdigit() and 1 <= int(choice) <= len(MENU):
            try:
                MENU[int(choice) - 1][1]()
            except (KeyboardInterrupt, EOFError):
                print("\n  ☯  Farewell.\n")
                return
        else:
            print("   Not a menu number.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  ☯  Farewell.\n")
        sys.exit(0)
