from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from enum import Enum
from typing import List


class ShiftType(Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    NIGHT = "Night"


@dataclass
class Shift:
    employee_id: str
    date: datetime
    shift_type: ShiftType

    def __post_init__(self):
        # normalize date to midnight for day-based comparisons
        self.date = self.date.replace(hour=0, minute=0, second=0, microsecond=0)

    def start_time(self) -> datetime:
        if self.shift_type == ShiftType.MORNING:
            return self.date.replace(hour=6)
        if self.shift_type == ShiftType.AFTERNOON:
            return self.date.replace(hour=14)
        # NIGHT
        return self.date.replace(hour=22)

    @property
    def start_time(self) -> datetime:
        return self._compute_times()[0]

    @property
    def end_time(self) -> datetime:
        return self._compute_times()[1]

    def _compute_times(self) -> tuple[datetime, datetime]:
        if self.shift_type == ShiftType.MORNING:
            start = self.date.replace(hour=6)
            end = self.date.replace(hour=14)
        elif self.shift_type == ShiftType.AFTERNOON:
            start = self.date.replace(hour=14)
            end = self.date.replace(hour=22)
        else:  # NIGHT
            start = self.date.replace(hour=22)
            end = (self.date + timedelta(days=1)).replace(hour=6)
        return start, end

    def duration_hours(self) -> float:
        start, end = self._compute_times()
        return (end - start).total_seconds() / 3600.0


@dataclass
class Employee:
    employee_id: str
    name: str
    shifts: List[Shift] = field(default_factory=list)

    def add_shift(self, shift: Shift) -> None:
        self.shifts.append(shift)

    def get_shifts_for_date(self, date: datetime) -> List[Shift]:
        target = date.replace(hour=0, minute=0, second=0, microsecond=0)
        return [s for s in self.shifts if s.date == target]

    def get_shifts_in_range(self, start: datetime, end: datetime) -> List[Shift]:
        start_day = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end_day = end.replace(hour=0, minute=0, second=0, microsecond=0)
        return [s for s in self.shifts if start_day <= s.date <= end_day]