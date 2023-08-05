"""
Policies for announcement scheduling.

Submissions to arXiv are normally made public on Sunday through Thursday, with
no announcements Friday or Saturday.

+-----------------------+----------------+------------------------------------+
| Received Between (ET) | Announced (ET) | Mailed                             |
+=======================+================+====================================+
| Mon 14:00 - Tue 14:00 | Tue 20:00      | Tuesday Night / Wednesday Morning  |
| Tue 14:00 - Wed 14:00 | Wed 20:00      | Wednesday Night / Thursday Morning |
| Wed 14:00 - Thu 14:00 | Thu 20:00      | Thursday Night / Friday Morning    |
| Thu 14:00 - Fri 14:00 | Sun 20:00      | Sunday Night / Monday Morning      |
| Fri 14:00 - Mon 14:00 | Mon 20:00      | Monday Night / Tuesday Morning     |
+-----------------------+----------------+------------------------------------+

"""

from typing import Optional
from datetime import datetime, timedelta
from enum import IntEnum, Enum
from pytz import timezone, UTC

ET = timezone('US/Eastern')


# I preferred the callable construction of IntEnum to the class-based
# construction, but this is more typing-friendly.
class Weekdays(IntEnum):
    """Numeric representation of the days of the week."""

    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
    Sun = 7


ANNOUNCE_TIME = 20   # Hours (8pm ET)
FREEZE_TIME = 14     # Hours (2pm ET)

WINDOWS = [
    ((Weekdays.Fri - 7, 14), (Weekdays.Mon, 14), (Weekdays.Mon, 20)),
    ((Weekdays.Mon, 14), (Weekdays.Tue, 14), (Weekdays.Tue, 20)),
    ((Weekdays.Tue, 14), (Weekdays.Wed, 14), (Weekdays.Wed, 20)),
    ((Weekdays.Wed, 14), (Weekdays.Thu, 14), (Weekdays.Thu, 20)),
    ((Weekdays.Thu, 14), (Weekdays.Fri, 14), (Weekdays.Sun, 20)),
    ((Weekdays.Fri, 14), (Weekdays.Mon + 7, 14), (Weekdays.Mon + 7, 20)),
]


def _datetime(ref: datetime, isoweekday: int, hour: int) -> datetime:
    days_hence = isoweekday - ref.isoweekday()
    # repl = dict(hour=hour, minute=0, second=0, microsecond=0)
    dt = (ref + timedelta(days=days_hence))
    return dt.replace(hour=hour, minute=0, second=0, microsecond=0)


def next_announcement_time(ref: Optional[datetime] = None) -> datetime:
    """Get the datetime of the next announcement."""
    if ref is None:
        ref = ET.localize(datetime.now())
    else:
        ref = ref.astimezone(ET)
    for start, end, announce in WINDOWS:
        if _datetime(ref, *start) <= ref < _datetime(ref, *end):
            return _datetime(ref, *announce)
    raise RuntimeError('Could not arrive at next announcement time')


def next_freeze_time(ref: Optional[datetime] = None) -> datetime:
    """Get the datetime of the next freeze."""
    if ref is None:
        ref = ET.localize(datetime.now())
    else:
        ref = ref.astimezone(ET)
    for start, end, announce in WINDOWS:
        if _datetime(ref, *start) <= ref < _datetime(ref, *end):
            return _datetime(ref, *end)
    raise RuntimeError('Could not arrive at next freeze time')
