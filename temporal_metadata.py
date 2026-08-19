#!/usr/bin/env python3
"""
Temporal Metadata & Real-Time Audit Timestamping Module (Python PSL ONLY).
Captures precise start/end timestamps, elapsed execution duration, timezone offsets,
and generates ISO 8601 & localized human-readable timestamps without external dependencies.
"""

import datetime
import os
import sys
import time
from typing import Dict, Any, Optional


def get_local_timezone_info(dt: Optional[datetime.datetime] = None) -> Dict[str, str]:
    """Extracts local timezone name and UTC offset string (e.g. '+02:00', 'CEST')."""
    if dt is None:
        dt = datetime.datetime.now().astimezone()
    else:
        if dt.tzinfo is None:
            dt = dt.astimezone()

    tz_name = dt.tzname() or "UTC"
    offset = dt.utcoffset()
    if offset is not None:
        total_seconds = int(offset.total_seconds())
        sign = "+" if total_seconds >= 0 else "-"
        abs_seconds = abs(total_seconds)
        hours = abs_seconds // 3600
        minutes = (abs_seconds % 3600) // 60
        tz_offset = f"{sign}{hours:02d}:{minutes:02d}"
    else:
        tz_offset = "+00:00"

    return {
        "timezone_name": tz_name,
        "timezone_offset": tz_offset
    }


class TemporalAuditMetadata:
    """Encapsulates execution timeline, duration, and timezone-aware timestamps."""

    def __init__(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        duration_sec: Optional[float] = None
    ):
        self.start_dt = (start_time or datetime.datetime.now()).astimezone()
        self.end_dt = end_time.astimezone() if end_time else None
        self._start_perf = time.perf_counter()
        self._duration_sec = duration_sec

        tz_info = get_local_timezone_info(self.start_dt)
        self.timezone_name = tz_info["timezone_name"]
        self.timezone_offset = tz_info["timezone_offset"]

    @classmethod
    def create_now(cls) -> "TemporalAuditMetadata":
        """Creates an initialized temporal tracker at the current instant."""
        return cls(start_time=datetime.datetime.now().astimezone())

    def finish(self, end_time: Optional[datetime.datetime] = None) -> "TemporalAuditMetadata":
        """Marks audit completion and computes elapsed duration."""
        if end_time:
            self.end_dt = end_time.astimezone()
            self._duration_sec = (self.end_dt - self.start_dt).total_seconds()
        else:
            self.end_dt = datetime.datetime.now().astimezone()
            self._duration_sec = max(0.0, time.perf_counter() - self._start_perf)
        return self

    @property
    def duration_sec(self) -> float:
        """Returns elapsed duration in seconds."""
        if self._duration_sec is not None:
            return self._duration_sec
        if self.end_dt:
            return max(0.0, (self.end_dt - self.start_dt).total_seconds())
        return max(0.0, time.perf_counter() - self._start_perf)

    @property
    def iso_start(self) -> str:
        """ISO 8601 formatted start timestamp (e.g. '2026-08-19T10:40:27+02:00')."""
        return self.start_dt.isoformat()

    @property
    def iso_end(self) -> str:
        """ISO 8601 formatted end timestamp."""
        dt = self.end_dt or self.start_dt
        return dt.isoformat()

    @property
    def localized_start(self) -> str:
        """Localized human-readable start timestamp (DD/MM/YYYY HH:MM:SS TZ)."""
        return f"{self.start_dt.strftime('%d/%m/%Y %H:%M:%S')} {self.timezone_name}"

    @property
    def localized_end(self) -> str:
        """Localized human-readable end timestamp (DD/MM/YYYY HH:MM:SS TZ)."""
        dt = self.end_dt or self.start_dt
        return f"{dt.strftime('%d/%m/%Y %H:%M:%S')} {self.timezone_name}"

    @property
    def standard_start(self) -> str:
        """Standard format (YYYY-MM-DD HH:MM:SS)."""
        return self.start_dt.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def standard_end(self) -> str:
        """Standard format (YYYY-MM-DD HH:MM:SS)."""
        dt = self.end_dt or self.start_dt
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def formatted_duration(self) -> str:
        """Human-readable duration format (e.g. '1.45s' or '250ms')."""
        dur = self.duration_sec
        if dur < 1.0:
            return f"{int(dur * 1000)}ms"
        return f"{dur:.2f}s"

    def to_dict(self) -> Dict[str, Any]:
        """Serializes temporal metadata to dictionary."""
        return {
            "iso_start": self.iso_start,
            "iso_end": self.iso_end,
            "localized_start": self.localized_start,
            "localized_end": self.localized_end,
            "standard_start": self.standard_start,
            "standard_end": self.standard_end,
            "duration_sec": round(self.duration_sec, 3),
            "formatted_duration": self.formatted_duration,
            "timezone_name": self.timezone_name,
            "timezone_offset": self.timezone_offset,
        }
