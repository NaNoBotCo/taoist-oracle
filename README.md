# Taoist Oracle

One engine for the Chinese/Taoist **cast-oracle** divination methods, built so
the deterministic-birth (Bazi, Zi Wei) and spatial (feng shui) layers can drop
in later without touching the core.

Pure Python standard library. Offline forever. No dependencies.

## Run

```
python3 oracle.py
```

Or double-click **`Taoist Oracle.command`** on the Desktop.

A numbered menu offers:

1. **I Ching 易經 — three coins** — quick cast, uniform odds.
2. **I Ching 易經 — yarrow stalks** — the authentic 49-stalk procedure, with the
   historical bias toward stable lines.
3. **Plum Blossom 梅花易數 — from two numbers** — you give two numbers; the
   engine builds the hexagram and the 體/用 (host/use) element reading.
4. **Plum Blossom 梅花易數 — from this moment** — the classic time method, using
   the current lunar date.
5. **Wen Wang Gua 文王卦 / Liu Yao 六爻** — a coin hexagram with its full overlay:
   najia branches (纳甲), five-element relatives (六親), world/response lines
   (世/應), the day's six beasts (六獸), and the void branches (旬空).

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

## What is complete vs. seeded

- **Mechanics: complete.** Every hexagram, changing line, transform, najia
  assignment, palace, six-relative, void, and the calendar are correct and
  tested.
- **Interpretation text: seeded.** Each hexagram has one concise gloss. The full
  384 line-texts are a data layer (`data/hexagrams.py` → `LINE_TEXTS`) left
  empty on purpose, ready to fill without touching the engine.

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
