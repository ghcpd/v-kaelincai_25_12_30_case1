"""Data models for the shift scheduling system."""

from datetime import datetime, timedelta
from enum import Enum
from typing import List


class ShiftType(Enum):
    """Types of shifts available."""
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"


class Shift:
    """Represents a single shift assignment."""
    
    # Shift timing constants
    MORNING_START = 6
    MORNING_END = 14
    AFTERNOON_START = 14
    AFTERNOON_END = 22
    NIGHT_START = 22
    NIGHT_END = 6  # Next day
    
    def __init__(self, employee_id: str, date: datetime, shift_type: ShiftType):
        """
        Initialize a shift.
        
        Args:
            employee_id: ID of the employee
            date: Date of the shift (time will be set based on shift_type)
            shift_type: Type of shift
        """
        self.employee_id = employee_id
        self.date = date.date()  # Store as date only
        self.shift_type = shift_type
        
        # Set start and end times based on shift type
        if shift_type == ShiftType.MORNING:
            self.start_time = datetime.combine(date.date(), datetime.min.time().replace(hour=self.MORNING_START))
            self.end_time = datetime.combine(date.date(), datetime.min.time().replace(hour=self.MORNING_END))
        elif shift_type == ShiftType.AFTERNOON:
            self.start_time = datetime.combine(date.date(), datetime.min.time().replace(hour=self.AFTERNOON_START))
            self.end_time = datetime.combine(date.date(), datetime.min.time().replace(hour=self.AFTERNOON_END))
        elif shift_type == ShiftType.NIGHT:
            self.start_time = datetime.combine(date.date(), datetime.min.time().replace(hour=self.NIGHT_START))
            self.end_time = datetime.combine(date.date() + timedelta(days=1), datetime.min.time().replace(hour=self.NIGHT_END))
    
    def duration_hours(self) -> float:
        """Calculate the duration of the shift in hours."""
        return (self.end_time - self.start_time).total_seconds() / 3600


class Employee:
    """Represents an employee and their assigned shifts."""
    
    def __init__(self, employee_id: str, name: str):
        """
        Initialize an employee.
        
        Args:
            employee_id: Unique identifier
            name: Employee name
        """
        self.employee_id = employee_id
        self.name = name
        self.shifts: List[Shift] = []
    
    def add_shift(self, shift: Shift):
        """Add a shift to the employee's schedule."""
        self.shifts.append(shift)
    
    def get_shifts_for_date(self, date) -> List[Shift]:
        """Get all shifts for a specific date."""
        return [s for s in self.shifts if s.date == date]
    
    def get_shifts_in_range(self, start_date, end_date) -> List[Shift]:
        """Get all shifts within a date range."""
        return [s for s in self.shifts if start_date <= s.date <= end_date]