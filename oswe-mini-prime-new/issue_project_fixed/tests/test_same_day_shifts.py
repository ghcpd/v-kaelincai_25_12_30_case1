"""
Test cases for same-day shift validation.

These tests verify that the system correctly enforces the business rule
that employees cannot have multiple shifts on the same day.
"""

import pytest
from datetime import datetime
from src.scheduler import ShiftScheduler
from src.models import ShiftType
from src.validator import ValidationError


class TestSameDayShifts:
    """Test suite for same-day shift validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.scheduler = ShiftScheduler()
        self.scheduler.add_employee("EMP001", "Li Ming")
    
    def test_morning_and_afternoon_same_day_should_fail(self):
        """
        Test that assigning both morning and afternoon shifts on the same day is rejected.
        
        This test verifies the business rule that employees cannot work multiple shifts
        on the same day.
        """
        date = datetime(2025, 1, 6)  # Monday
        
        # Assign morning shift - should succeed
        self.scheduler.assign_shift("EMP001", date, ShiftType.MORNING)
        
        # Try to assign afternoon shift on the SAME day - should FAIL
        with pytest.raises(ValidationError, match="already has a .* shift on"):
            self.scheduler.assign_shift("EMP001", date, ShiftType.AFTERNOON)
    
    def test_morning_and_night_same_day_should_fail(self):
        """
        Test that assigning both morning and night shifts on the same day is rejected.
        
        This test verifies the business rule enforcement.
        """
        date = datetime(2025, 1, 7)  # Tuesday
        
        # Assign morning shift
        self.scheduler.assign_shift("EMP001", date, ShiftType.MORNING)
        
        # Try to assign night shift on the SAME day - should FAIL
        with pytest.raises(ValidationError, match="already has a .* shift on"):
            self.scheduler.assign_shift("EMP001", date, ShiftType.NIGHT)
    
    def test_afternoon_and_night_same_day_should_fail(self):
        """
        Test that assigning both afternoon and night shifts on the same day is rejected.
        """
        date = datetime(2025, 1, 8)  # Wednesday
        
        # Assign afternoon shift
        self.scheduler.assign_shift("EMP001", date, ShiftType.AFTERNOON)
        
        # Try to assign night shift on the SAME day - should FAIL
        with pytest.raises(ValidationError, match="already has a .* shift on"):
            self.scheduler.assign_shift("EMP001", date, ShiftType.NIGHT)
    
    def test_different_days_should_succeed(self):
        """
        Test that assigning shifts on different days is allowed (this should PASS).
        """
        date1 = datetime(2025, 1, 6)
        date2 = datetime(2025, 1, 7)
        
        # These should both succeed - different days
        shift1 = self.scheduler.assign_shift("EMP001", date1, ShiftType.MORNING)
        shift2 = self.scheduler.assign_shift("EMP001", date2, ShiftType.AFTERNOON)
        
        assert shift1.date != shift2.date
        assert len(self.scheduler.get_employee("EMP001").shifts) == 2
    
    def test_same_shift_type_same_day_should_also_fail(self):
        """
        Test that assigning the same shift type twice on the same day is also rejected.
        """
        date = datetime(2025, 1, 9)  # Thursday
        
        # Assign morning shift
        self.scheduler.assign_shift("EMP001", date, ShiftType.MORNING)
        
        # Try to assign another morning shift on the SAME day - should FAIL
        with pytest.raises(ValidationError, match="already has a .* shift on"):
            self.scheduler.assign_shift("EMP001", date, ShiftType.MORNING)
