"""Main shift scheduler module."""

from datetime import datetime
from typing import Dict
from src.models import Employee, Shift, ShiftType
from src.validator import ShiftValidator, ValidationError


class ShiftScheduler:
    """Manages employee shift scheduling with validation."""
    
    def __init__(self):
        """Initialize the scheduler."""
        self.employees: Dict[str, Employee] = {}
    
    def add_employee(self, employee_id: str, name: str) -> Employee:
        """
        Add a new employee to the system.
        
        Args:
            employee_id: Unique identifier
            name: Employee name
            
        Returns:
            The created Employee object
        """
        employee = Employee(employee_id, name)
        self.employees[employee_id] = employee
        return employee
    
    def get_employee(self, employee_id: str) -> Employee:
        """
        Get an employee by ID.
        
        Args:
            employee_id: Employee identifier
            
        Returns:
            Employee object
            
        Raises:
            KeyError: If employee not found
        """
        if employee_id not in self.employees:
            raise KeyError(f"Employee {employee_id} not found")
        return self.employees[employee_id]
    
    def assign_shift(self, employee_id: str, date: datetime, shift_type: ShiftType) -> Shift:
        """
        Assign a shift to an employee after validation.
        
        Args:
            employee_id: Employee to assign shift to
            date: Date of the shift
            shift_type: Type of shift (morning/afternoon/night)
            
        Returns:
            The created Shift object
            
        Raises:
            ValidationError: If shift violates business rules
            KeyError: If employee not found
        """
        employee = self.get_employee(employee_id)
        
        # Create the shift
        new_shift = Shift(employee_id, date, shift_type)
        
        # Validate the shift
        validator = ShiftValidator(employee)
        validator.validate_new_shift(new_shift)
        
        # If validation passes, add the shift
        employee.add_shift(new_shift)
        
        return new_shift
    
    def get_employee_schedule(self, employee_id: str) -> list:
        """
        Get all shifts for an employee.
        
        Args:
            employee_id: Employee identifier
            
        Returns:
            List of Shift objects sorted by date
        """
        employee = self.get_employee(employee_id)
        return sorted(employee.shifts, key=lambda s: s.start_time)