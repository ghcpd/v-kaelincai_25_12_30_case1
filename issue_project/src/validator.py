"""Validation rules for shift scheduling.

This module contains the business rules that must be validated before assigning shifts.
"""

from datetime import datetime, timedelta
from typing import List
from src.models import Shift, Employee, ShiftType


class ValidationError(Exception):
    """Exception raised when a shift assignment violates a rule."""
    pass


class ShiftValidator:
    """Validates shift assignments against business rules."""
    
    # Business rule constants
    MAX_CONSECUTIVE_DAYS = 6
    MIN_REST_HOURS_AFTER_NIGHT = 12
    MAX_WEEKLY_HOURS = 48
    
    def __init__(self, employee: Employee):
        """
        Initialize validator for an employee.
        
        Args:
            employee: The employee whose shifts will be validated
        """
        self.employee = employee
    
    def validate_new_shift(self, new_shift: Shift) -> bool:
        """
        Validate if a new shift can be added to the employee's schedule.
        
        Args:
            new_shift: The shift to validate
            
        Returns:
            True if shift is valid
            
        Raises:
            ValidationError: If the shift violates any rule
        """
        self._validate_consecutive_days(new_shift)
        self._validate_night_shift_rest(new_shift)
        self._validate_weekly_hours(new_shift)
        
        return True
    
    def _validate_same_day_shifts(self, new_shift: Shift):
        """
        Validate that employee doesn't have another shift on the same day.
        """
        existing_shifts = self.employee.get_shifts_for_date(new_shift.date)
        if existing_shifts:
            raise ValidationError(
                f"Employee {self.employee.employee_id} already has a {existing_shifts[0].shift_type.value} "
                f"shift on {new_shift.date.date()}. Cannot assign multiple shifts on the same day."
            )
    
    def _validate_consecutive_days(self, new_shift: Shift):
        """Validate that employee doesn't work more than 6 consecutive days."""
        if not self.employee.shifts:
            return
        
        # Sort existing shifts by date
        sorted_shifts = sorted(self.employee.shifts, key=lambda s: s.date)
        
        # Check consecutive days before the new shift
        consecutive_count = 0
        check_date = new_shift.date - timedelta(days=1)
        
        for i in range(self.MAX_CONSECUTIVE_DAYS):
            has_shift = any(s.date == check_date for s in sorted_shifts)
            if has_shift:
                consecutive_count += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        if consecutive_count >= self.MAX_CONSECUTIVE_DAYS:
            raise ValidationError(
                f"Employee {self.employee.employee_id} has already worked {consecutive_count} "
                f"consecutive days. Must rest at least 1 day."
            )
    
    def _validate_night_shift_rest(self, new_shift: Shift):
        """Validate 12-hour rest period after night shifts."""
        # Check if there's a night shift before this shift
        for existing_shift in self.employee.shifts:
            if existing_shift.shift_type == ShiftType.NIGHT:
                # Night shift ends at 06:00 the next day
                hours_between = (new_shift.start_time - existing_shift.end_time).total_seconds() / 3600
                
                if 0 < hours_between < self.MIN_REST_HOURS_AFTER_NIGHT:
                    raise ValidationError(
                        f"Employee {self.employee.employee_id} needs {self.MIN_REST_HOURS_AFTER_NIGHT} hours "
                        f"rest after night shift ending {existing_shift.end_time}. "
                        f"Only {hours_between:.1f} hours before next shift."
                    )
    
    def _validate_weekly_hours(self, new_shift: Shift):
        """Validate that weekly working hours don't exceed 48 hours."""
        # Calculate the week start (Monday) for the new shift
        days_since_monday = new_shift.date.weekday()
        week_start = new_shift.date - timedelta(days=days_since_monday)
        week_end = week_start + timedelta(days=6)
        
        # Get all shifts in the same week
        week_shifts = self.employee.get_shifts_in_range(week_start, week_end)
        
        # Calculate total hours including the new shift
        total_hours = sum(s.duration_hours() for s in week_shifts) + new_shift.duration_hours()
        
        if total_hours > self.MAX_WEEKLY_HOURS:
            raise ValidationError(
                f"Employee {self.employee.employee_id} would exceed weekly limit of {self.MAX_WEEKLY_HOURS} hours. "
                f"Current: {total_hours - new_shift.duration_hours():.1f}h, "
                f"New shift: {new_shift.duration_hours()}h, "
                f"Total: {total_hours:.1f}h"
            )
