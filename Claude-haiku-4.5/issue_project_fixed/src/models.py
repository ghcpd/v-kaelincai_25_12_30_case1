"""Data models for the shift scheduling system."""

from enum import Enum
from datetime import datetime, timedelta
from typing import List


class ShiftType(Enum):
    """Types of shifts available."""
    MORNING = "morning"      # 06:00 - 14:00
    AFTERNOON = "afternoon"  # 14:00 - 22:00
    NIGHT = "night"          # 22:00 - 06:00 (next day)


class Shift:
    """Represents a work shift for an employee."""
    
    # Define shift times
    SHIFT_TIMES = {
        ShiftType.MORNING: {"start": "06:00", "end": "14:00"},
        ShiftType.AFTERNOON: {"start": "14:00", "end": "22:00"},
        ShiftType.NIGHT: {"start": "22:00", "end": "06:00"},  # Ends next day
    }
    
    def __init__(self, employee_id: str, date: datetime, shift_type: ShiftType):
        """
        Initialize a shift.
        
        Args:
            employee_id: Employee assigned to this shift
            date: Date of the shift (for Night shift, this is the start date)
            shift_type: Type of shift (morning/afternoon/night)
        """
        self.employee_id = employee_id
        self.date = date
        self.shift_type = shift_type
        
        # Set start and end times based on shift type
        if shift_type == ShiftType.MORNING:
            self.start_time = date.replace(hour=6, minute=0, second=0, microsecond=0)
            self.end_time = date.replace(hour=14, minute=0, second=0, microsecond=0)
        elif shift_type == ShiftType.AFTERNOON:
            self.start_time = date.replace(hour=14, minute=0, second=0, microsecond=0)
            self.end_time = date.replace(hour=22, minute=0, second=0, microsecond=0)
        elif shift_type == ShiftType.NIGHT:
            self.start_time = date.replace(hour=22, minute=0, second=0, microsecond=0)
            # Night shift ends at 06:00 the next day
            self.end_time = (date + timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)
    
    def duration_hours(self) -> float:
        """Get the duration of this shift in hours."""
        return (self.end_time - self.start_time).total_seconds() / 3600
    
    def __repr__(self) -> str:
        """String representation of the shift."""
        return f"Shift({self.employee_id}, {self.date.date()}, {self.shift_type.value})"


class Employee:
    """Represents an employee in the system."""
    
    def __init__(self, employee_id: str, name: str):
        """
        Initialize an employee.
        
        Args:
            employee_id: Unique identifier for the employee
            name: Employee's name
        """
        self.employee_id = employee_id
        self.name = name
        self.shifts: List[Shift] = []
    
    def add_shift(self, shift: Shift) -> None:
        """
        Add a shift to the employee's schedule.
        
        Args:
            shift: The shift to add
        """
        self.shifts.append(shift)
    
    def get_shifts_for_date(self, date: datetime) -> List[Shift]:
        """
        Get all shifts for a specific date.
        
        Args:
            date: The date to check (compared by date only, not time)
            
        Returns:
            List of shifts on that date
        """
        return [s for s in self.shifts if s.date.date() == date.date()]
    
    def get_shifts_in_range(self, start_date: datetime, end_date: datetime) -> List[Shift]:
        """
        Get all shifts within a date range.
        
        Args:
            start_date: Start of the range (inclusive)
            end_date: End of the range (inclusive)
            
        Returns:
            List of shifts in the range
        """
        return [
            s for s in self.shifts 
            if start_date.date() <= s.date.date() <= end_date.date()
        ]
    
    def __repr__(self) -> str:
        """String representation of the employee."""
        return f"Employee({self.employee_id}, {self.name})"
