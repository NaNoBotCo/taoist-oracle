# Taoist Oracle

One engine for the Chinese/Taoist divination methods — the **cast oracles** (I
Ching, Plum Blossom, Wen Wang Gua) and the first **deterministic birth chart**
(Bazi / Four Pillars) — with the remaining layers (Zi Wei, feng shui, the Three
Styles) designed to drop in without touching the core.

Pure Python standard library. Offline forever. No dependencies.

## Run

```
python3 oracle.py
```

Or double-click **`Taoist Oracle.command`** on the Desktop.

A numbered menu offers:

1. **I Ching 易經 — three coins** — quick cast, symmetric odds.
2. **I Ching 易經 — yarrow stalks** — draws each line from the traditional
   yarrow distribution, with the historical bias toward stable lines.

   **The odds shift** (menu item 6, or the "About the odds" panel in the web
   version): both methods give the same 50/50 yin–yang balance and the same 25%
   chance a line is moving. The coin method only changes the *internal lean* —
   yarrow favors stable young-yin and, among moving lines, old-yang over old-yin
   3:1; coins flatten that to perfect symmetry.

   | line | yarrow | three coins |
   |---|---|---|
   | 9 老陽 old yang (moving) | 18.75% | 12.5% |
   | 8 少陰 young yin | 43.75% | 37.5% |
   | 7 少陽 young yang | 31.25% | 37.5% |
   | 6 老陰 old yin (moving) | 6.25% | 12.5% |
3. **Plum Blossom 梅花易數 — from two numbers** — you give two numbers; the
   engine builds the hexagram and the 體/用 (host/use) element reading.
4. **Plum Blossom 梅花易數 — from this moment** — the classic time method, using
   the current lunar date.
5. **Wen Wang Gua 文王卦 / Liu Yao 六爻** — a coin hexagram with its full overlay:
   najia branches (纳甲), five-element relatives (六親), world/response lines
   (世/應), the day's six beasts (六獸), and the void branches (旬空).
6. **Bazi 八字 / Four Pillars** — a birth moment → four solar-term-bounded Ganzhi
   pillars, the Day Master (日主), hidden stems (藏干), the Ten Gods (十神), nayin
   (納音), the five-element tally, and the 大運 luck pillars. All exact rule-based
   computation; the day-master strength read is a *labelled heuristic*, not a
   verdict (real 用神 assessment is an interpretive craft). Methods in
   `methods/bazi.py`.

## Architecture

The whole tradition rests on a few shared engines. Build them once, reuse
everywhere — that is the point of this project.

```
core/
  bagua.py        8 trigrams, 64 hexagrams, King Wen order, hexagram ops
  wuxing.py       Five Elements: generating / overcoming, six-relative logic
  ganzhi.py       sexagenary cycle, the four pillars, void branches
  calendar_cn.py  pure-Python lunisolar calendar + 24 solar terms (astronomy)
  luoshu.py       the 3x3 magic square (spine for the future feng-shui layer)
methods/
  yijing.py       yarrow + coin casting
  meihua.py       Plum Blossom (numbers and time)
  liuyao.py       Wen Wang Gua overlay (najia, eight palaces, six beasts)
data/
  hexagrams.py    the King Wen table, trigram pairs, concise glosses
oracle.py         the numbered-menu console
tests.py          self-tests (run: python3 tests.py)
```

### The calendar

Everything time-based needs two astronomical facts: the Sun's ecliptic
longitude (the 24 solar terms) and the instants of New Moon (the lunar months).
Both are computed with Meeus low-precision series (accurate to ~1 minute for the
modern era), then assembled into the civil Chinese calendar with the standard
rules (month 11 contains the December solstice; a leap month is the first month
of a 13-month solar year with no major solar term). Validated against real
Chinese New Years 2020–2033 and the 2023 leap-2nd-month.

## Interpretation — grounded in the canonical texts

The I Ching reading is not invented. It draws on the received tradition:

- **`data/zhouyi.json`** holds the verbatim canonical **卦辭 (Judgment)** and all
  **384 爻辭 (line statements)** of the Zhou Yi, plus 用九/用六 for 乾 and 坤 —
  sourced from ctext.org (public domain) — each paired with a concise **English
  translation of my own**, clearly marked as such (not Legge, not Wilhelm).
- Every reading shows the Judgment and **all six lines** with their 爻辭, the
  **moving lines highlighted** (they carry the answer), plus the classical
  **reading protocol** (which lines to read, by how many are moving) and the
  **位/中/正/應 line-position doctrine**, labeled as traditional line theory.
- `build_web.py` injects the corpus into `oracle.html`; the Python CLI loads the
  same JSON. One source of truth for both surfaces.

## The web version also has

- a **question/intention field** — held with each reading and the journal;
- a **journal** of past readings (stored in your browser only);
- a **"Which method, when?"** guidance panel;
- the subtle **yarrow ritual animation** and the **odds** explainer.

## What is complete

Every hexagram, changing line, transform, najia assignment, palace,
six-relative, void, the calendar, and the full canonical text are correct and
tested.

## Extending

- **Cast oracles**: add a module in `methods/`, reuse the spine.
- **Bazi / Zi Wei (deterministic)**: `ganzhi.four_pillars()` already returns all
  four pillars for any moment — the birth-chart layer builds directly on it.
- **Feng shui (spatial)**: `luoshu.py` holds the flying order the Flying Star and
  Eight Mansions methods need.

The methods are two projections of one graph: chance-cast oracles and
time-derived systems both read the same trigram / element / cycle primitives.

## Scope note

"Taoist" here is the loose popular grouping. Several methods (Bazi, the almanac,
feng shui) are Chinese cosmological rather than strictly Daoist; they share the
same engines, which is why one codebase covers them.


## Licence

Records, prose and pages: CC BY-SA 4.0. Code: AGPL-3.0-or-later. Anything
carried in from elsewhere keeps its own terms — see [LICENSE](LICENSE).

**Commercial licence.** If share-alike doesn't fit your use — a corpus, a
product, a model — a commercial licence is available.
[Open an issue](https://github.com/NaNoBotCo/taoist-oracle/issues) and say what you need.
