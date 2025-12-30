"""Data models for the shift scheduler (Employee, Shift, ShiftType).

This implementation provides the minimal API expected by the scheduler,
validator and the tests in this kata.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List


class ShiftType(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"


@dataclass
class Shift:
    employee_id: str
    date: datetime
    shift_type: ShiftType

    def __post_init__(self):
        # derive concrete start/end datetimes from the date and shift type
        d = self.date.replace(hour=0, minute=0, second=0, microsecond=0)
        if self.shift_type == ShiftType.MORNING:
            self.start_time = d.replace(hour=6)
            self.end_time = d.replace(hour=14)
        elif self.shift_type == ShiftType.AFTERNOON:
            self.start_time = d.replace(hour=14)
            self.end_time = d.replace(hour=22)
        else:  # NIGHT
            self.start_time = d.replace(hour=22)
            # night shift ends next day at 06:00
            self.end_time = (d + timedelta(days=1)).replace(hour=6)

    def duration_hours(self) -> int:
        return int((self.end_time - self.start_time).total_seconds() / 3600)


@dataclass
class Employee:
    employee_id: str
    name: str
    shifts: List[Shift] = field(default_factory=list)

    def add_shift(self, shift: Shift) -> None:
        # small convenience: ensure the shift references this employee
        shift.employee_id = self.employee_id
        self.shifts.append(shift)

    def get_shifts_for_date(self, date: datetime) -> List[Shift]:
        target = date.date()
        # same-day rule should consider the *assigned* shift date only
        # (a night shift assigned to the previous date that ends after midnight
        # should NOT be treated as a shift "on" the next calendar day for this
        # particular business rule — the night-rest rule covers that case).
        return [s for s in self.shifts if s.date.date() == target]

    def get_shifts_in_range(self, start: datetime, end: datetime) -> List[Shift]:
        start_date = start.date()
        end_date = end.date()
        return [s for s in self.shifts if start_date <= s.start_time.date() <= end_date]
