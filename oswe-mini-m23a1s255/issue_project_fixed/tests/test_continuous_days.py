"""
Test cases for consecutive days validation.

These tests verify that the consecutive days rule is working correctly.
These tests should PASS (this rule is correctly implemented).
"""

import pytest
from datetime import datetime, timedelta
from src.scheduler import ShiftScheduler
from src.models import ShiftType
from src.validator import ValidationError


class TestConsecutiveDays:
    """Test suite for consecutive days validation (these should PASS)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.scheduler = ShiftScheduler()
        self.scheduler.add_employee("EMP002", "Zhang Wei")
    
    def test_six_consecutive_days_allowed(self):
        """
        Test that working 6 consecutive days is allowed (at the limit).
        This test should PASS.
        """
        start_date = datetime(2025, 1, 6)  # Monday
        
        # Assign 6 consecutive days of morning shifts
        for i in range(6):
            date = start_date + timedelta(days=i)
            self.scheduler.assign_shift("EMP002", date, ShiftType.MORNING)
        
        employee = self.scheduler.get_employee("EMP002")
        assert len(employee.shifts) == 6
    
    def test_seven_consecutive_days_rejected(self):
        """
        Test that working 7 consecutive days is rejected.
        This test should PASS (validation works correctly).
        """
        start_date = datetime(2025, 1, 6)  # Monday
        
        # Assign 6 consecutive days - should succeed
        for i in range(6):
            date = start_date + timedelta(days=i)
            self.scheduler.assign_shift("EMP002", date, ShiftType.MORNING)
        
        # Try to assign 7th consecutive day - should be REJECTED
        seventh_day = start_date + timedelta(days=6)
        with pytest.raises(ValidationError, match="already worked .* consecutive days"):
            self.scheduler.assign_shift("EMP002", seventh_day, ShiftType.MORNING)
    
    def test_rest_day_resets_counter(self):
        """
        Test that a rest day resets the consecutive days counter.
        This test should PASS.
        """
        start_date = datetime(2025, 1, 6)  # Monday
        
        # Work 3 days
        for i in range(3):
            date = start_date + timedelta(days=i)
            self.scheduler.assign_shift("EMP002", date, ShiftType.MORNING)
        
        # Rest day (skip day 3)
        # Then work 6 more days starting from day 4 - should be allowed
        for i in range(4, 10):
            date = start_date + timedelta(days=i)
            self.scheduler.assign_shift("EMP002", date, ShiftType.MORNING)
        
        employee = self.scheduler.get_employee("EMP002")
        assert len(employee.shifts) == 9  # 3 + 6


class TestWeeklyHours:
    """Test suite for weekly hours validation (should PASS)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.scheduler = ShiftScheduler()
        self.scheduler.add_employee("EMP003", "Liu Qiang")
    
    def test_48_hours_per_week_allowed(self):
        """
        Test that exactly 48 hours per week is allowed.
        This test should PASS.
        """
        # Monday of week
        monday = datetime(2025, 1, 6)
        
        # Assign 6 shifts of 8 hours each = 48 hours
        for i in range(6):
            date = monday + timedelta(days=i)
            self.scheduler.assign_shift("EMP003", date, ShiftType.MORNING)
        
        employee = self.scheduler.get_employee("EMP003")
        assert len(employee.shifts) == 6
    
    def test_exceed_48_hours_rejected(self):
        """
        Test that exceeding 48 hours per week is rejected.
        This test should PASS.
        """
        monday = datetime(2025, 1, 6)
        
        # Assign 6 shifts (48 hours total)
        for i in range(6):
            date = monday + timedelta(days=i)
            self.scheduler.assign_shift("EMP003", date, ShiftType.MORNING)
        
        # Try to add 7th shift (would be 56 hours) - should be REJECTED
        sunday = monday + timedelta(days=6)
        with pytest.raises(ValidationError, match="exceed weekly limit"):
            self.scheduler.assign_shift("EMP003", sunday, ShiftType.AFTERNOON)


class TestNightShiftRest:
    """Test suite for night shift rest period validation (should PASS)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.scheduler = ShiftScheduler()
        self.scheduler.add_employee("EMP004", "Wang Fang")
    
    def test_12_hour_rest_after_night_shift_required(self):
        """
        Test that 12-hour rest after night shift is enforced.
        This test should PASS.
        """
        # Tuesday night shift (22:00 Tue to 06:00 Wed)
        tuesday = datetime(2025, 1, 7)
        self.scheduler.assign_shift("EMP004", tuesday, ShiftType.NIGHT)
        
        # Try to assign Wednesday morning shift (starts 06:00) - only 0 hours rest!
        wednesday = datetime(2025, 1, 8)
        with pytest.raises(ValidationError, match="needs 12 hours rest after night shift"):
            self.scheduler.assign_shift("EMP004", wednesday, ShiftType.MORNING)
    
    def test_sufficient_rest_after_night_shift_allowed(self):
        """
        Test that shifts with sufficient rest after night shift are allowed.
        This test should PASS.
        """
        # Monday night shift (22:00 Mon to 06:00 Tue)
        monday = datetime(2025, 1, 6)
        self.scheduler.assign_shift("EMP004", monday, ShiftType.NIGHT)
        
        # Wednesday morning shift (starts 06:00 Wed) - 48 hours rest, OK
        wednesday = datetime(2025, 1, 8)
        shift = self.scheduler.assign_shift("EMP004", wednesday, ShiftType.MORNING)
        
        assert shift is not None
        employee = self.scheduler.get_employee("EMP004")
        assert len(employee.shifts) == 2
