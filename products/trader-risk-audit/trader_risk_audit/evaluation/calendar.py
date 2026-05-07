from __future__ import annotations

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo


def assign_session_date(
    timestamp: datetime,
    *,
    timezone: str,
    session_start: str,
) -> date:
    if timestamp.tzinfo is None:
        raise ValueError("timestamp must include timezone")

    local_timestamp = timestamp.astimezone(ZoneInfo(timezone))
    start_time = time.fromisoformat(session_start)
    session_date = local_timestamp.date()
    if local_timestamp.time() < start_time:
        session_date -= timedelta(days=1)
    return session_date
