#!/usr/bin/env python
"""Functional validation test for the shift scheduler bug fix."""

from src.scheduler import ShiftScheduler
from src.models import ShiftType
from src.validator import ValidationError
from datetime import datetime

print("=" * 70)
print("FUNCTIONAL VALIDATION TEST - Same-Day Shift Prevention")
print("=" * 70)

scheduler = ShiftScheduler()
scheduler.add_employee("EMP001", "Li Ming")

print("\n[TEST 1] Assigning morning shift on 2025-01-06...")
date = datetime(2025, 1, 6)
try:
    shift1 = scheduler.assign_shift("EMP001", date, ShiftType.MORNING)
    print(f"✓ SUCCESS: {shift1}")
except ValidationError as e:
    print(f"✗ FAILED: {e}")
    exit(1)

print("\n[TEST 2] Attempting to assign afternoon shift on SAME day (2025-01-06)...")
try:
    shift2 = scheduler.assign_shift("EMP001", date, ShiftType.AFTERNOON)
    print(f"✗ FAILED: Should have been rejected but was assigned: {shift2}")
    exit(1)
except ValidationError as e:
    print(f"✓ SUCCESS (Correctly Rejected): {str(e)[:80]}...")

print("\n[TEST 3] Assigning afternoon shift on DIFFERENT day (2025-01-07)...")
date2 = datetime(2025, 1, 7)
try:
    shift3 = scheduler.assign_shift("EMP001", date2, ShiftType.AFTERNOON)
    print(f"✓ SUCCESS: {shift3}")
except ValidationError as e:
    print(f"✗ FAILED: {e}")
    exit(1)

print("\n[TEST 4] Verifying employee schedule...")
schedule = scheduler.get_employee_schedule("EMP001")
print(f"Total shifts: {len(schedule)}")
for shift in schedule:
    print(f"  • {shift}")

if len(schedule) != 2:
    print(f"✗ FAILED: Expected 2 shifts, got {len(schedule)}")
    exit(1)

print("\n" + "=" * 70)
print("FUNCTIONAL VALIDATION: ✓ ALL TESTS PASSED - BUG IS FIXED!")
print("=" * 70)
