"""
Test cases for consecutive days validation (copied from original).
"""

import pytest
from datetime import datetime, timedelta
from src.scheduler import ShiftScheduler
from src.models import ShiftType
from src.validator import ValidationError


class TestConsecutiveDays:
    def setup_method(self):
        self.scheduler = ShiftScheduler()
        self.scheduler.add_employee("EMP002", "Zhang Wei")

    def test_six_consecutive_days_allowed(self):
        start_date = datetime(2025, 1, 6)
        for i in range(6):
            date = start_date + timedelta(days=i)
            self.scheduler.assign_shift("EMP002", date, ShiftType.MORNING)
        employee = self.scheduler.get_employee("EMP002")
        assert len(employee.shifts) == 6

    def test_seven_consecutive_days_rejected(self):
        start_date = datetime(2025, 1, 6)
        for i in range(6):
            date = start_date + timedelta(days=i)
            self.scheduler.assign_shift("EMP002", date, ShiftType.MORNING)
        seventh_day = start_date + timedelta(days=6)
        with pytest.raises(ValidationError, match="already worked .* consecutive days"):
            self.scheduler.assign_shift("EMP002", seventh_day, ShiftType.MORNING)

    def test_rest_day_resets_counter(self):
        start_date = datetime(2025, 1, 6)
        for i in range(3):
            date = start_date + timedelta(days=i)
            self.scheduler.assign_shift("EMP002", date, ShiftType.MORNING)
        for i in range(4, 10):
            date = start_date + timedelta(days=i)
            self.scheduler.assign_shift("EMP002", date, ShiftType.MORNING)
        employee = self.scheduler.get_employee("EMP002")
        assert len(employee.shifts) == 9


class TestWeeklyHours:
    def setup_method(self):
        self.scheduler = ShiftScheduler()
        self.scheduler.add_employee("EMP003", "Liu Qiang")

    def test_48_hours_per_week_allowed(self):
        monday = datetime(2025, 1, 6)
        for i in range(6):
            date = monday + timedelta(days=i)
            self.scheduler.assign_shift("EMP003", date, ShiftType.MORNING)
        employee = self.scheduler.get_employee("EMP003")
        assert len(employee.shifts) == 6

    def test_exceed_48_hours_rejected(self):
        monday = datetime(2025, 1, 6)
        for i in range(6):
            date = monday + timedelta(days=i)
            self.scheduler.assign_shift("EMP003", date, ShiftType.MORNING)
        sunday = monday + timedelta(days=6)
        with pytest.raises(ValidationError, match="exceed weekly limit"):
            self.scheduler.assign_shift("EMP003", sunday, ShiftType.AFTERNOON)


class TestNightShiftRest:
    def setup_method(self):
        self.scheduler = ShiftScheduler()
        self.scheduler.add_employee("EMP004", "Wang Fang")

    def test_12_hour_rest_after_night_shift_required(self):
        tuesday = datetime(2025, 1, 7)
        self.scheduler.assign_shift("EMP004", tuesday, ShiftType.NIGHT)
        wednesday = datetime(2025, 1, 8)
        with pytest.raises(ValidationError, match="needs 12 hours rest after night shift"):
            self.scheduler.assign_shift("EMP004", wednesday, ShiftType.MORNING)

    def test_sufficient_rest_after_night_shift_allowed(self):
        monday = datetime(2025, 1, 6)
        self.scheduler.assign_shift("EMP004", monday, ShiftType.NIGHT)
        wednesday = datetime(2025, 1, 8)
        shift = self.scheduler.assign_shift("EMP004", wednesday, ShiftType.MORNING)
        assert shift is not None
        employee = self.scheduler.get_employee("EMP004")
        assert len(employee.shifts) == 2