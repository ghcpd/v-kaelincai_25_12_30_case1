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
        employee = Employee(employee_id, name)
        self.employees[employee_id] = employee
        return employee
    
    def get_employee(self, employee_id: str) -> Employee:
        if employee_id not in self.employees:
            raise KeyError(f"Employee {employee_id} not found")
        return self.employees[employee_id]
    
    def assign_shift(self, employee_id: str, date: datetime, shift_type: ShiftType) -> Shift:
        employee = self.get_employee(employee_id)
        
        new_shift = Shift(employee_id, date, shift_type)
        
        validator = ShiftValidator(employee)
        validator.validate_new_shift(new_shift)
        
        employee.add_shift(new_shift)
        
        return new_shift
    
    def get_employee_schedule(self, employee_id: str) -> list:
        employee = self.get_employee(employee_id)
        return sorted(employee.shifts, key=lambda s: s.start_time)