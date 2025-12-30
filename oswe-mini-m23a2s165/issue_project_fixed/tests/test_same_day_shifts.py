"""
Test cases for same-day shift validation (copied from original).
"""

import pytest
from datetime import datetime
from src.scheduler import ShiftScheduler
from src.models import ShiftType
from src.validator import ValidationError


class TestSameDayShifts:
    def setup_method(self):
        self.scheduler = ShiftScheduler()
        self.scheduler.add_employee("EMP001", "Li Ming")

    def test_morning_and_afternoon_same_day_should_fail(self):
        date = datetime(2025, 1, 6)
        self.scheduler.assign_shift("EMP001", date, ShiftType.MORNING)
        with pytest.raises(ValidationError, match="already has a .* shift on"):
            self.scheduler.assign_shift("EMP001", date, ShiftType.AFTERNOON)

    def test_morning_and_night_same_day_should_fail(self):
        date = datetime(2025, 1, 7)
        self.scheduler.assign_shift("EMP001", date, ShiftType.MORNING)
        with pytest.raises(ValidationError, match="already has a .* shift on"):
            self.scheduler.assign_shift("EMP001", date, ShiftType.NIGHT)

    def test_afternoon_and_night_same_day_should_fail(self):
        date = datetime(2025, 1, 8)
        self.scheduler.assign_shift("EMP001", date, ShiftType.AFTERNOON)
        with pytest.raises(ValidationError, match="already has a .* shift on"):
            self.scheduler.assign_shift("EMP001", date, ShiftType.NIGHT)

    def test_different_days_should_succeed(self):
        date1 = datetime(2025, 1, 6)
        date2 = datetime(2025, 1, 7)
        shift1 = self.scheduler.assign_shift("EMP001", date1, ShiftType.MORNING)
        shift2 = self.scheduler.assign_shift("EMP001", date2, ShiftType.AFTERNOON)
        assert shift1.date != shift2.date
        assert len(self.scheduler.get_employee("EMP001").shifts) == 2

    def test_same_shift_type_same_day_should_also_fail(self):
        date = datetime(2025, 1, 9)
        self.scheduler.assign_shift("EMP001", date, ShiftType.MORNING)
        with pytest.raises(ValidationError, match="already has a .* shift on"):
            self.scheduler.assign_shift("EMP001", date, ShiftType.MORNING)