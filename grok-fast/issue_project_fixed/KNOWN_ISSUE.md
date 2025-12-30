# Known Issue: Same-Day Shift Constraint Violation

## Issue Summary

**Issue ID**: BUG-001  
**Type**: Functional Bug - Constraint Violation  
**Severity**: High  
**Status**: Reproduced, Not Fixed  
**Discovered**: December 30, 2025

## Problem Description

The shift scheduler system allows assigning multiple shifts to the same employee on the same day, which violates the core business rule:

> **Business Rule**: An employee cannot have more than one shift on the same day (e.g., cannot work both morning and afternoon shifts on the same day).

### Impact

- **Business Impact**: Employees may be scheduled for 16 hours of work in a single day (e.g., morning + afternoon, or afternoon + night)
- **Compliance Risk**: Violates labor regulations regarding maximum daily working hours
- **User Experience**: System accepts invalid schedules without warning
- **Data Integrity**: Database contains impossible shift combinations

## Root Cause Analysis

### Primary Cause

The shift validation logic is incomplete. Some validation methods exist in the codebase but are not properly integrated into the validation pipeline.

### Technical Details

**Symptom**: Same-day shift assignments are accepted without validation
**Category**: Missing validation call
**Complexity**: Simple - the validation logic exists but isn't being used

**Hint**: Look carefully at the validation workflow in the validator module. Compare which validation methods exist versus which ones are actually called during shift assignment.

## Debugging Approach

### How to Investigate

1. **Run the tests** to see which specific scenarios fail
2. **Read the test expectations** to understand what should happen
3. **Trace the code flow** from `scheduler.assign_shift()` through to the validator
4. **Examine all validation methods** - what exists vs. what gets executed
5. **Use print statements or debugger** to see the execution path

### Questions to Ask

- What happens when `assign_shift()` is called?
- Which validation methods exist in the `ShiftValidator` class?
- Which validation methods are actually called during shift assignment?
- Is there a gap between what exists and what executes?

## Reproduction Steps

### Minimal Reproduction

```python
from src.scheduler import ShiftScheduler
from src.models import ShiftType
from datetime import datetime

scheduler = ShiftScheduler()
scheduler.add_employee("EMP001", "Li Ming")

# Step 1: Assign morning shift
date = datetime(2025, 1, 6)
shift1 = scheduler.assign_shift("EMP001", date, ShiftType.MORNING)
print(f"✓ Assigned: {shift1}")

# Step 2: Assign afternoon shift on SAME day - should fail but doesn't!
shift2 = scheduler.assign_shift("EMP001", date, ShiftType.AFTERNOON)
print(f"✓ Assigned: {shift2}")  # BUG: This should have raised ValidationError!

# Result: Employee has TWO shifts on the same day (16 hours of work!)
```

### Expected Behavior
```
✓ Assigned: Shift(EMP001, 2025-01-06, morning)
✗ ValidationError: Employee EMP001 already has a morning shift on 2025-01-06. 
  Cannot assign multiple shifts on the same day.
```

### Actual Behavior
```
✓ Assigned: Shift(EMP001, 2025-01-06, morning)
✓ Assigned: Shift(EMP001, 2025-01-06, afternoon)
```

## Test Evidence

### Failing Tests

Run the following command to see the failures:
```powershell
pytest tests/test_same_day_shifts.py -v
```

**5 tests demonstrate the bug**:
1. `test_morning_and_afternoon_same_day_should_fail` - FAILS
2. `test_morning_and_night_same_day_should_fail` - FAILS
3. `test_afternoon_and_night_same_day_should_fail` - FAILS
4. `test_same_shift_type_same_day_should_also_fail` - FAILS
5. `test_different_days_should_succeed` - PASSES (correctly allows different days)

### Test Output Example
```
FAILED tests/test_same_day_shifts.py::TestSameDayShifts::test_morning_and_afternoon_same_day_should_fail

Expected ValidationError to be raised with message matching "already has a .* shift on"
But no exception was raised - both shifts were successfully assigned!
```

## Expected Behavior After Fix

### Validation Should Work

After applying the fix:

```powershell
# All same-day shift tests should now PASS
pytest tests/test_same_day_shifts.py -v

# All other tests should still PASS
pytest tests/test_continuous_days.py -v

# Full test suite
pytest -v
```

**Expected Results**: 10/10 tests pass

## Why This Bug Exists

This is a classic example of a **functional bug** where:
- The business requirement was understood
- The validation logic was correctly implemented
- BUT the validation was never integrated into the execution flow

**Common Causes**:
- Code was written but not wired up
- Developer forgot to call the validation method
- Incomplete code review
- Missing integration tests at the time of development
- Copy-paste error from template code

## Lessons Learned

1. **Test-Driven Development**: Writing tests first would have caught this immediately
2. **Code Coverage**: 100% line coverage ≠ 100% logic coverage (the method exists but isn't called)
3. **Integration Testing**: Unit tests on `_validate_same_day_shifts()` alone would pass, but integration tests reveal the bug
4. **Code Review**: Reviewers should verify that validation methods are actually invoked
5. **Static Analysis**: Could potentially detect "dead code" (unused private methods)

## Related Files

- **Validation Logic**: `src/validator.py`
- **Test Suite**: `tests/test_same_day_shifts.py`
- **Scheduler Logic**: `src/scheduler.py`
- **Data Models**: `src/models.py`

## References

- Business Requirements: See README.md "Business Rules" section
- Test Documentation: See test docstrings in `test_same_day_shifts.py`
- Validation Architecture: See `validator.py` module documentation
