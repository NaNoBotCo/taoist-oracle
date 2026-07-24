"""Chinese lunisolar calendar + 24 solar terms, in pure Python.

Everything time-based in the tradition rests on two astronomical facts:
    - the Sun's apparent ecliptic longitude  (the 24 solar terms 節氣)
    - the instants of New Moon                (the lunar months)

We compute both with Meeus low-precision series (accurate to ~1 minute for the
modern era), then assemble the civil Chinese calendar with the standard rules:
month boundaries at New Moons, month 11 contains the December solstice, and a
leap month is the first month of a 13-month solar year that has no major solar
term (中氣 zhongqi).

All civil dates are assigned in China Standard Time (UTC+8), the calendar's
legal reference meridian. ΔT is neglected (sub-minute effect on day assignment).
"""

import math

PI = math.pi
RAD = PI / 180.0
CST = 8.0 / 24.0   # China Standard Time offset, in days


# --------------------------------------------------------------------------
# Julian day
# --------------------------------------------------------------------------
def gregorian_to_jd(year, month, day, hour=0.0):
    """Proleptic-Gregorian calendar date -> Julian Day (float, at given UT hour)."""
    y, m = year, month
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4
    jd = (math.floor(365.25 * (y + 4716))
          + math.floor(30.6001 * (m + 1))
          + day + b - 1524.5)
    return jd + hour / 24.0


def jd_to_gregorian(jd):
    """Julian Day -> (year, month, day_float) in the Gregorian calendar."""
    jd = jd + 0.5
    z = math.floor(jd)
    f = jd - z
    if z < 2299161:
        a = z
    else:
        alpha = math.floor((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - alpha // 4
    b = a + 1524
    c = math.floor((b - 122.1) / 365.25)
    d = math.floor(365.25 * c)
    e = math.floor((b - d) / 30.6001)
    day = b - d - math.floor(30.6001 * e) + f
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    return year, month, day


def jd_to_civil_date(jd):
    """JD -> (year, month, day) integers, in China Standard Time."""
    y, m, d = jd_to_gregorian(jd + CST)
    return y, m, int(math.floor(d))


# --------------------------------------------------------------------------
# Sun: apparent ecliptic longitude (Meeus, ch. 25, low precision)
# --------------------------------------------------------------------------
def solar_longitude(jd):
    """Apparent geocentric ecliptic longitude of the Sun in degrees [0,360)."""
    t = (jd - 2451545.0) / 36525.0
    l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t
    m = 357.52911 + 35999.05029 * t - 0.0001537 * t * t
    mr = m * RAD
    c = ((1.914602 - 0.004817 * t - 0.000014 * t * t) * math.sin(mr)
         + (0.019993 - 0.000101 * t) * math.sin(2 * mr)
         + 0.000289 * math.sin(3 * mr))
    true_long = l0 + c
    omega = 125.04 - 1934.136 * t
    app = true_long - 0.00569 - 0.00478 * math.sin(omega * RAD)
    return app % 360.0


def solar_term_jd(target_deg, approx_jd):
    """JD at which apparent solar longitude equals target_deg (0..360),
    searched from approx_jd. Newton iteration on the ~0.9856 deg/day rate."""
    jd = approx_jd
    for _ in range(50):
        diff = (target_deg - solar_longitude(jd) + 180.0) % 360.0 - 180.0
        if abs(diff) < 1e-7:
            break
        jd += diff / 0.98565
    return jd


def term_jd_for_year(year, target_deg):
    """JD of the solar term at target_deg occurring in the given Gregorian
    year (each 15-deg longitude occurs once per year). Seeds the search from a
    linear estimate then converges."""
    # Sun is at 280 deg near Jan 1; roughly target crosses at this day-of-year.
    approx_day = ((target_deg - 280.0) % 360.0) / 0.98565
    approx = gregorian_to_jd(year, 1, 1) + approx_day
    return solar_term_jd(target_deg, approx)


# The 24 terms, in longitude order starting at the December solstice.
SOLAR_TERMS = [
    (270, "冬至", "Winter Solstice"), (285, "小寒", "Minor Cold"),
    (300, "大寒", "Major Cold"),      (315, "立春", "Start of Spring"),
    (330, "雨水", "Rain Water"),      (345, "驚蟄", "Awakening of Insects"),
    (0,   "春分", "Spring Equinox"),  (15,  "清明", "Clear and Bright"),
    (30,  "穀雨", "Grain Rain"),      (45,  "立夏", "Start of Summer"),
    (60,  "小滿", "Grain Full"),      (75,  "芒種", "Grain in Ear"),
    (90,  "夏至", "Summer Solstice"), (105, "小暑", "Minor Heat"),
    (120, "大暑", "Major Heat"),      (135, "立秋", "Start of Autumn"),
    (150, "處暑", "End of Heat"),     (165, "白露", "White Dew"),
    (180, "秋分", "Autumn Equinox"),  (195, "寒露", "Cold Dew"),
    (210, "霜降", "Frost Descent"),   (225, "立冬", "Start of Winter"),
    (240, "小雪", "Minor Snow"),      (255, "大雪", "Major Snow"),
]


def current_solar_term(jd):
    """The most recent solar term at or before jd: (deg, hanzi, english)."""
    lon = solar_longitude(jd)
    idx = int(((lon - 270) % 360) // 15)
    return SOLAR_TERMS[idx]


# --------------------------------------------------------------------------
# Moon: instants of New Moon (Meeus, ch. 49)
# --------------------------------------------------------------------------
def newmoon_jd(k):
    """JD (Dynamical Time ~ UT here) of the k-th New Moon after 2000-01-06."""
    t = k / 1236.85
    jde = (2451550.09766 + 29.530588861 * k
           + 0.00015437 * t * t
           - 0.000000150 * t ** 3
           + 0.00000000073 * t ** 4)
    m = 2.5534 + 29.10535670 * k - 0.0000014 * t * t - 0.00000011 * t ** 3
    mp = 201.5643 + 385.81693528 * k + 0.0107582 * t * t + 0.00001238 * t ** 3
    f = 160.7108 + 390.67050284 * k - 0.0016118 * t * t - 0.00000227 * t ** 3
    om = 124.7746 - 1.56375588 * k + 0.0020672 * t * t + 0.00000215 * t ** 3
    e = 1 - 0.002516 * t - 0.0000074 * t * t
    m *= RAD; mp *= RAD; f *= RAD; om *= RAD

    corr = (-0.40720 * math.sin(mp)
            + 0.17241 * e * math.sin(m)
            + 0.01608 * math.sin(2 * mp)
            + 0.01039 * math.sin(2 * f)
            + 0.00739 * e * math.sin(mp - m)
            - 0.00514 * e * math.sin(mp + m)
            + 0.00208 * e * e * math.sin(2 * m)
            - 0.00111 * math.sin(mp - 2 * f)
            - 0.00057 * math.sin(mp + 2 * f)
            + 0.00056 * e * math.sin(2 * mp + m)
            - 0.00042 * math.sin(3 * mp)
            + 0.00042 * e * math.sin(m + 2 * f)
            + 0.00038 * e * math.sin(m - 2 * f)
            - 0.00024 * e * math.sin(2 * mp - m)
            - 0.00017 * math.sin(om)
            - 0.00007 * math.sin(mp + 2 * m)
            + 0.00004 * math.sin(2 * mp - 2 * f)
            + 0.00004 * math.sin(3 * m)
            + 0.00003 * math.sin(mp + m - 2 * f)
            + 0.00003 * math.sin(2 * mp + 2 * f)
            - 0.00003 * math.sin(mp + m + 2 * f)
            + 0.00003 * math.sin(mp - m + 2 * f)
            - 0.00002 * math.sin(mp - m - 2 * f)
            - 0.00002 * math.sin(3 * mp + m)
            + 0.00002 * math.sin(4 * mp))
    return jde + corr


def _k_near(jd):
    return round((jd - 2451550.09766) / 29.530588861)


def _nm_day_start(k):
    """CST-midnight JD of the civil day containing the k-th New Moon."""
    nm = newmoon_jd(k) + CST
    y, m, d = jd_to_gregorian(nm)
    return _midnight_jd(y, m, int(math.floor(d)))


def newmoon_on_or_before(jd):
    """CST-midnight JD of the New-Moon day at or before civil-midnight jd."""
    k = _k_near(jd)
    while _nm_day_start(k) > jd + 0.5:
        k -= 1
    while _nm_day_start(k + 1) <= jd + 0.5:
        k += 1
    return _nm_day_start(k)


# --------------------------------------------------------------------------
# Assemble the civil lunisolar calendar
# --------------------------------------------------------------------------
def _midnight_jd(year, month, day):
    """JD at CST midnight starting the given civil date."""
    return gregorian_to_jd(year, month, day) - CST


def _winter_solstice_jd(year):
    """CST JD of the day containing the December solstice of `year`."""
    j = term_jd_for_year(year, 270) + CST
    y, m, d = jd_to_gregorian(j)
    return _midnight_jd(y, m, int(math.floor(d)))


def _month_starts(from_jd, to_jd):
    """CST-midnight JDs of New-Moon days whose day falls in [from_jd, to_jd]."""
    starts = []
    k = _k_near(from_jd) - 2
    while True:
        day0 = _nm_day_start(k)
        if day0 > to_jd:
            break
        if day0 >= from_jd - 0.5:
            starts.append(day0)
        k += 1
    return starts


def _has_major_term(month_start, next_start):
    """True if a major solar term (中氣, longitude a multiple of 30 deg) falls
    within [month_start, next_start). Since solar longitude increases
    monotonically, this is exactly a crossing of a 30-deg mark between the two
    civil-midnight boundaries."""
    l0 = solar_longitude(month_start)
    l1 = solar_longitude(next_start)
    if l1 < l0:
        l1 += 360.0
    return math.floor(l1 / 30.0) > math.floor(l0 / 30.0)


def lunar_date(year, month, day):
    """Gregorian (civil) date -> dict with lunar year, month (1..12),
    is_leap, day (1..30)."""
    target = _midnight_jd(year, month, day)

    # Establish the two winter-solstice months bracketing this date.
    # Month 11 is the lunar month that contains the December solstice.
    ws_year = year if target >= _winter_solstice_jd(year) else year - 1
    ws_prev = _winter_solstice_jd(ws_year)
    ws_next = _winter_solstice_jd(ws_year + 1)

    m11_start = newmoon_on_or_before(ws_prev)          # start of month 11
    next_m11_start = newmoon_on_or_before(ws_next)     # start of the next 11

    starts = _month_starts(m11_start - 1, next_m11_start + 40)
    # keep the run beginning at m11_start
    starts = [s for s in starts if s >= m11_start - 0.5]
    starts.sort()

    # number of months in this solar year (from one m11 to the next, exclusive)
    months_in_year = 0
    for s in starts:
        if m11_start - 0.5 <= s < next_m11_start - 0.5:
            months_in_year += 1

    leap_needed = months_in_year == 13
    leap_assigned = False
    labels = []       # (start, month_number, is_leap, next_start)
    month_no = 11
    last_num = 11
    for i, s in enumerate(starts):
        nxt = starts[i + 1] if i + 1 < len(starts) else s + 30
        is_leap = False
        if leap_needed and not leap_assigned and i > 0:
            if not _has_major_term(s, nxt):
                is_leap = True
                leap_assigned = True
        if is_leap:
            num = last_num                 # a leap month carries the prior number
        else:
            num = month_no
            last_num = month_no
            month_no = 1 if month_no == 12 else month_no + 1
        labels.append((s, num, is_leap, nxt))

    # find the month containing target
    chosen = labels[0]
    for lab in labels:
        if lab[0] - 0.5 <= target < lab[3] - 0.5:
            chosen = lab
            break

    start, mnum, is_leap, _ = chosen
    lday = int(round(target - start)) + 1

    # lunar civil year: the year of the New-Year (month-1) start
    # months 11,12 of the run belong to the previous lunar year
    lyear = ws_year + 1
    if mnum >= 11:
        lyear = ws_year
    return {
        "year": lyear,
        "month": mnum,
        "is_leap": is_leap,
        "day": lday,
    }
