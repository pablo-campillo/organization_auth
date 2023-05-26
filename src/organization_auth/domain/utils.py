from datetime import datetime, timezone


def my_utc_now():
    return datetime.now(timezone.utc)
