from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4

# Python 3.9+ has zoneinfo; otherwise you might use pytz.
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback to pytz if needed (note that the API differs slightly)
    from pytz import timezone as ZoneInfo

# Optionally, you may want to use dateutil.parser for flexible string parsing.
try:
    from dateutil import parser
except ImportError:
    parser = None

# Assuming these are part of your framework:
from pythings.__base__ import (BaseEntity, Entity, BaseAttribute, BaseAbstractEntity,
                               BasePhysicalEntity, BaseRelationship)


class TimePoint(BaseAbstractEntity):
    """
    Represents an instantaneous moment in time.
    Uses an internal datetime object that can be timezone-aware.
    """

    def __init__(self, dt, name: str = 'time point', description: str = '', uid: str | UUID = None) -> None:
        """
        :param dt: A datetime.datetime instance (aware or naive).
        :param name: A human-readable name.
        :param description: An optional description.
        :param uid: A unique identifier (auto-generated if None).
        """
        uid = uid or uuid4()
        super().__init__(identifier=uid, label=name, description=description, sumo_class="TimePoint")
        if not isinstance(dt, datetime):
            raise ValueError("TimePoint must be initialized with a datetime object.")
        self._datetime = dt

    @property
    def datetime(self) -> datetime:
        """Returns the underlying datetime object."""
        return self._datetime

    def to_timezone(self, tz: str | ZoneInfo) -> "TimePoint":
        """
        Returns a new TimePoint converted to the given timezone.
        :param tz: A timezone name (e.g. 'UTC', 'America/New_York') or a ZoneInfo object.
        """
        if isinstance(tz, str):
            tz = ZoneInfo(tz)
        new_dt = self._datetime.astimezone(tz)
        return TimePoint(new_dt, name=self.label, description=self.description, uid=self.identifier)

    def to_isoformat(self) -> str:
        """Returns an ISO 8601 string representation of the underlying datetime."""
        return self._datetime.isoformat()

    @classmethod
    def from_isoformat(cls, dt_str: str, name: str = 'time point', description: str = '',
                       uid: str | UUID = None) -> "TimePoint":
        """Creates a TimePoint from an ISO 8601 formatted string."""
        dt = datetime.fromisoformat(dt_str)
        return cls(dt, name, description, uid or uuid4())

    @classmethod
    def from_string(cls, dt_str: str, fmt: str = None, name: str = 'time point', description: str = '',
                    uid: str | UUID = None) -> "TimePoint":
        """
        Creates a TimePoint from a string.
        If a format is provided, datetime.strptime is used; otherwise, dateutil.parser.parse is attempted.
        """
        if fmt:
            dt = datetime.strptime(dt_str, fmt)
        elif parser:
            dt = parser.parse(dt_str)
        else:
            raise ValueError("No format provided and dateutil.parser is not available.")
        return cls(dt, name, description, uid or uuid4())

    def to_pendulum(self):
        """Convert to a pendulum.DateTime instance if pendulum is installed."""
        try:
            import pendulum
        except ImportError:
            raise ImportError("pendulum is not installed")
        return pendulum.instance(self._datetime)

    def __add__(self, other):
        """Add a timedelta to this TimePoint, returning a new TimePoint."""
        if isinstance(other, timedelta):
            return TimePoint(self._datetime + other, name=self.label, description=self.description)
        raise TypeError("Can only add timedelta to TimePoint")

    def __sub__(self, other):
        """
        Subtract a timedelta or another TimePoint.
        If subtracting a TimePoint, returns a timedelta.
        """
        if isinstance(other, timedelta):
            return TimePoint(self._datetime - other, name=self.label, description=self.description)
        elif isinstance(other, TimePoint):
            return self._datetime - other._datetime
        else:
            raise TypeError("Unsupported operand type for TimePoint subtraction.")

    def __lt__(self, other):
        if isinstance(other, TimePoint):
            return self._datetime < other._datetime
        raise TypeError("Comparisons only supported between TimePoint instances.")

    def __le__(self, other):
        if isinstance(other, TimePoint):
            return self._datetime <= other._datetime
        raise TypeError("Comparisons only supported between TimePoint instances.")

    def __eq__(self, other):
        if isinstance(other, TimePoint):
            return self._datetime == other._datetime
        return False

    def __gt__(self, other):
        if isinstance(other, TimePoint):
            return self._datetime > other._datetime
        raise TypeError("Comparisons only supported between TimePoint instances.")

    def __ge__(self, other):
        if isinstance(other, TimePoint):
            return self._datetime >= other._datetime
        raise TypeError("Comparisons only supported between TimePoint instances.")

    def __repr__(self):
        return f"TimePoint({self._datetime.isoformat()})"


class FuzzyTimePoint(TimePoint):
    """
    Represents a time point with uncertainty (e.g. 'around 3 PM' with a tolerance).
    """

    def __init__(self, dt, tolerance: timedelta, name: str = 'fuzzy time point', description: str = '',
                 uid: str | UUID = None):
        super().__init__(dt, name, description, uid or uuid4())
        if not isinstance(tolerance, timedelta):
            raise ValueError("tolerance must be a timedelta")
        self.tolerance = tolerance

    def __repr__(self):
        return f"FuzzyTimePoint({self._datetime.isoformat()} ± {self.tolerance})"


class TimeInterval(BaseAbstractEntity):
    """
    Represents a time interval defined by a start and an end TimePoint.
    Optionally, a 'confidence' level (from 0 to 1) can indicate uncertainty.
    """

    def __init__(self, start, end, name: str = 'time interval', description: str = '', uid: str | UUID = None,
                 confidence: float = 1.0):
        uid = uid or uuid4()
        super().__init__(identifier=uid, label=name, description=description, sumo_class="TimeInterval")
        if not isinstance(start, TimePoint) or not isinstance(end, TimePoint):
            raise ValueError("Both start and end must be TimePoint instances.")
        if start >= end:
            raise ValueError("Start TimePoint must be earlier than end TimePoint.")
        self.start = start
        self.end = end
        self.confidence = confidence

    def duration(self, unit: str = 'timedelta'):
        """
        Returns the duration of the interval.
        :param unit: One of 'timedelta', 'seconds', 'minutes', 'hours', or 'human' (for a human-readable string).
        """
        delta = self.end.datetime - self.start.datetime
        if unit == 'timedelta':
            return delta
        elif unit == 'seconds':
            return delta.total_seconds()
        elif unit == 'minutes':
            return delta.total_seconds() / 60
        elif unit == 'hours':
            return delta.total_seconds() / 3600
        elif unit == 'human':
            seconds = int(delta.total_seconds())
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            parts = []
            if hours:
                parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if minutes:
                parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
            if seconds:
                parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
            return ', '.join(parts)
        else:
            raise ValueError("Unsupported unit. Choose 'timedelta', 'seconds', 'minutes', 'hours', or 'human'.")

    def contains(self, time_point):
        """Checks if a given TimePoint falls within this interval (inclusive)."""
        if not isinstance(time_point, TimePoint):
            raise ValueError("Argument must be a TimePoint instance.")
        return self.start <= time_point <= self.end

    def overlaps(self, other):
        """
        Checks if this interval overlaps with another TimeInterval.
        Two intervals overlap if one starts before the other ends
        and the other starts before the first ends.
        """
        if not isinstance(other, TimeInterval):
            raise ValueError("Argument must be a TimeInterval instance.")
        return self.start < other.end and other.start < self.end

    # --- Additional Temporal Relations ---
    def meets(self, other) -> bool:
        """Returns True if self ends exactly when other begins."""
        if not isinstance(other, TimeInterval):
            raise ValueError("Argument must be a TimeInterval instance.")
        return self.end == other.start

    def met_by(self, other) -> bool:
        """Returns True if self starts exactly when other ends."""
        return other.meets(self)

    def starts_relation(self, other) -> bool:
        """
        Returns True if this interval starts at the same moment as the other,
        but ends earlier.
        """
        if not isinstance(other, TimeInterval):
            raise ValueError("Argument must be a TimeInterval instance.")
        return self.start == other.start and self.end < other.end

    def started_by(self, other) -> bool:
        return other.starts_relation(self)

    def finishes(self, other) -> bool:
        """
        Returns True if this interval ends at the same moment as the other,
        but starts later.
        """
        if not isinstance(other, TimeInterval):
            raise ValueError("Argument must be a TimeInterval instance.")
        return self.end == other.end and self.start > other.start

    def finished_by(self, other) -> bool:
        return other.finishes(self)

    def during(self, other) -> bool:
        """
        Returns True if this interval is completely contained within the other.
        """
        if not isinstance(other, TimeInterval):
            raise ValueError("Argument must be a TimeInterval instance.")
        return self.start > other.start and self.end < other.end

    # --- Interval Arithmetic ---
    def intersection(self, other) -> Optional["TimeInterval"]:
        """
        Returns a new TimeInterval representing the intersection of this interval and another,
        or None if they do not overlap.
        """
        if not isinstance(other, TimeInterval):
            raise ValueError("Argument must be a TimeInterval instance.")
        if not self.overlaps(other):
            return None
        new_start = max(self.start, other.start)
        new_end = min(self.end, other.end)
        return TimeInterval(new_start, new_end, name=f"Intersection of {self.label} and {other.label}")

    def union(self, other) -> Optional["TimeInterval"]:
        """
        Returns a new TimeInterval representing the union of this interval and another
        if they overlap or meet; otherwise, returns None.
        """
        if not isinstance(other, TimeInterval):
            raise ValueError("Argument must be a TimeInterval instance.")
        if self.overlaps(other) or self.meets(other) or self.met_by(other):
            new_start = min(self.start, other.start)
            new_end = max(self.end, other.end)
            return TimeInterval(new_start, new_end, name=f"Union of {self.label} and {other.label}")
        return None

    def difference(self, other) -> list:
        """
        Returns a list of TimeIntervals representing parts of self that are not within other.
        The result may be empty (if other completely covers self), one interval, or two intervals.
        """
        if not isinstance(other, TimeInterval):
            raise ValueError("Argument must be a TimeInterval instance.")
        result = []
        if not self.overlaps(other):
            result.append(self)
            return result
        # If other fully covers self, no remainder.
        if other.start <= self.start and other.end >= self.end:
            return result
        # Portion before other starts.
        if other.start > self.start:
            result.append(TimeInterval(self.start, min(other.start, self.end), name=f"{self.label} diff part 1"))
        # Portion after other ends.
        if other.end < self.end:
            result.append(TimeInterval(max(other.end, self.start), self.end, name=f"{self.label} diff part 2"))
        return result

    # --- Interval Splitting and Iteration ---
    def split(self, sub_duration: timedelta) -> list:
        """
        Splits the interval into consecutive subintervals of duration 'sub_duration'.
        The last subinterval may be shorter if the interval does not divide evenly.
        """
        if sub_duration <= timedelta(0):
            raise ValueError("sub_duration must be positive.")
        intervals = []
        current_start = self.start
        while current_start + sub_duration <= self.end:
            current_end = current_start + sub_duration
            intervals.append(TimeInterval(current_start, current_end, name=f"{self.label} chunk"))
            current_start = current_end
        if current_start < self.end:
            intervals.append(TimeInterval(current_start, self.end, name=f"{self.label} last chunk"))
        return intervals

    def iter_timepoints(self, step: timedelta):
        """
        Yields TimePoint objects from the start to the end of the interval at each 'step'.
        """
        current = self.start
        while current <= self.end:
            yield current
            current = current + step

    def __repr__(self):
        conf_str = f" (confidence={self.confidence})" if self.confidence < 1.0 else ""
        return f"TimeInterval(start={self.start}, end={self.end}){conf_str}"


# --- Example Usage ---
if __name__ == "__main__":
    from time import sleep

    # Create TimePoints with current time
    now = TimePoint(datetime.now())
    one_hour_later = TimePoint(datetime.now() + timedelta(hours=1))

    # Demonstrate arithmetic with TimePoint
    fifteen_minutes_later = now + timedelta(minutes=15)
    print("Now:", now)
    print("15 minutes later:", fifteen_minutes_later)
    print("Difference (as timedelta):", one_hour_later - now)

    # Create a TimeInterval
    meeting_interval = TimeInterval(start=now, end=one_hour_later, name="Meeting")
    print("\nMeeting Interval:", meeting_interval)
    print("Duration (human):", meeting_interval.duration(unit='human'))

    # Create another interval that overlaps the meeting
    later_interval = TimeInterval(
        start=TimePoint(datetime.now() + timedelta(minutes=30)),
        end=TimePoint(datetime.now() + timedelta(hours=1, minutes=30)),
        name="Later Event"
    )
    print("\nLater Interval:", later_interval)
    print("Do intervals overlap?", meeting_interval.overlaps(later_interval))
    print("Intersection:", meeting_interval.intersection(later_interval))
    print("Union:", meeting_interval.union(later_interval))
    print("Difference (Meeting minus Later):", meeting_interval.difference(later_interval))

    # Demonstrate additional temporal relations
    contiguous_interval = TimeInterval(
        start=one_hour_later,
        end=TimePoint(datetime.now() + timedelta(hours=2)),
        name="Contiguous Event"
    )
    print("\nContiguous Interval:", contiguous_interval)
    print("Meeting meets Contiguous?", meeting_interval.meets(contiguous_interval))
    print("Contiguous met_by Meeting?", contiguous_interval.met_by(meeting_interval))

    # Splitting an interval into 15-minute slots:
    slots = meeting_interval.split(timedelta(minutes=15))
    print("\nMeeting split into 15-minute slots:")
    for slot in slots:
        print(f"  {slot.start.to_isoformat()} to {slot.end.to_isoformat()}")

    # Example of using a fuzzy time point:
    fuzzy_time = FuzzyTimePoint(datetime.now(), tolerance=timedelta(minutes=10))
    print("\nFuzzy TimePoint example:", fuzzy_time)
