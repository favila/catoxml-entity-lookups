from datetime import datetime, timedelta, tzinfo

ZERO = timedelta(0)


class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

UTC = UTC()


def now():
    """Return datetime object in UTC without microseconds"""
    return datetime.utcnow().replace(microsecond=0, tzinfo=UTC)


def now_isoformat():
    """Return current UTC time as an iso-formatted string"""
    return now().isoformat()
