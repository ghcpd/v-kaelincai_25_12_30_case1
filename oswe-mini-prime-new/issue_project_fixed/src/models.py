from __future__ import annotations

from datetime import datetime, time, timedelta
from enum import Enum
from typing import List


class ShiftType(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"


class Shift:
    """Represents a single shift for an employee."""

    DURATION = timedelta(hours=8)

    def __init__(self, employee_id: str, date: datetime, shift_type: ShiftType):
        self.employee_id = employee_id
        # Normalize date to midnight for easy same-day comparisons
        self.date = datetime(date.year, date.month, date.day)
        self.shift_type = shift_type

        # Compute start_time and end_time based on shift type
        if shift_type == ShiftType.MORNING:
            self.start_time = datetime(self.date.year, self.date.month, self.date.day, 6, 0)
            self.end_time = self.start_time + Shift.DURATION
        elif shift_type == ShiftType.AFTERNOON:
            self.start_time = datetime(self.date.year, self.date.month, self.date.day, 14, 0)
            self.end_time = self.start_time + Shift.DURATION
        elif shift_type == ShiftType.NIGHT:
            # Night shift spans into the next day
            self.start_time = datetime(self.date.year, self.date.month, self.date.day, 22, 0)
            self.end_time = self.start_time + Shift.DURATION
        else:
            raise ValueError("Unknown shift type")

    def duration_hours(self) -> int:
        return int(Shift.DURATION.total_seconds() / 3600)

    def __repr__(self):
        return f"<Shift {self.shift_type.value} {self.date.date()} for {self.employee_id}>"


class Employee:
    """Represents an employee and their assigned shifts."""

    def __init__(self, employee_id: str, name: str):
        self.employee_id = employee_id
        self.name = name
        self.shifts: List[Shift] = []

    def add_shift(self, shift: Shift):
        self.shifts.append(shift)

    def get_shifts_for_date(self, date: datetime) -> List[Shift]:
        target = datetime(date.year, date.month, date.day)
        return [s for s in self.shifts if s.date == target]

    def get_shifts_in_range(self, start: datetime, end: datetime) -> List[Shift]:
        start_day = datetime(start.year, start.month, start.day)
        end_day = datetime(end.year, end.month, end.day)
        return [s for s in self.shifts if start_day <= s.date <= end_day]
