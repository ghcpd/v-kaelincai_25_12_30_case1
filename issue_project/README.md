# Shift Scheduler System - Bug Reproduction Project

A minimal employee shift scheduling system with **intentionally planted bugs** for testing and debugging practice.

## Project Overview

This project implements a factory production line shift scheduling system with the following business rules:

### Business Rules
1. ✅ **Max Consecutive Days**: Employees cannot work more than 6 consecutive days without rest
2. ✅ **Night Shift Rest**: After a night shift (22:00-06:00), employees must rest at least 12 hours
3. ✅ **Weekly Hours Limit**: Employees cannot exceed 48 hours of work per week
4. ❌ **Same-Day Single Shift**: Employees cannot have multiple shifts on the same day (BROKEN!)

### Shift Types
- **Morning**: 06:00 - 14:00 (8 hours)
- **Afternoon**: 14:00 - 22:00 (8 hours)
- **Night**: 22:00 - 06:00 next day (8 hours)

## Project Structure

```
shift_scheduler/
├── src/
│   ├── __init__.py
│   ├── models.py          # Employee and Shift data models
│   ├── scheduler.py       # Main scheduling logic
│   └── validator.py       # Business rule validation (BUG HERE!)
├── tests/
│   ├── __init__.py
│   ├── test_same_day_shifts.py      # FAILING tests - expose the bug
│   └── test_continuous_days.py      # PASSING tests - other rules work
├── data/
│   └── sample_shifts.json           # Sample data demonstrating the bug
├── requirements.txt
├── README.md
└── KNOWN_ISSUE.md         # Detailed bug analysis
```

## The Bug 🐛

**Type**: Functional Bug - Constraint Violation

**Issue**: The system allows assigning multiple shifts to the same employee on the same day, violating the business rule.

**Location**: Somewhere in the validation pipeline - you need to find it!

**Root Cause**: A validation method exists but is not properly integrated into the validation workflow. Your job is to discover which validation is missing and why.

## Quick Start

### Installation

```powershell
# Install dependencies
pip install -r requirements.txt
```

### Run Tests

```powershell
# Run all tests (some will FAIL - this is expected!)
pytest -v

# Run only the failing tests (same-day validation)
pytest tests/test_same_day_shifts.py -v

# Run only the passing tests (other rules)
pytest tests/test_continuous_days.py -v
```

### Expected Output

When you run the tests, you should see:

- ✅ **5 tests PASS** - Other validation rules work correctly
- ❌ **5 tests FAIL** - Same-day shift validation is broken

Example output:
```
tests/test_same_day_shifts.py::TestSameDayShifts::test_morning_and_afternoon_same_day_should_fail FAILED
tests/test_same_day_shifts.py::TestSameDayShifts::test_morning_and_night_same_day_should_fail FAILED
tests/test_continuous_days.py::TestConsecutiveDays::test_six_consecutive_days_allowed PASSED
tests/test_continuous_days.py::TestConsecutiveDays::test_seven_consecutive_days_rejected PASSED
...
```

## Bug Reproduction Steps

1. Create an employee:
   ```python
   from src.scheduler import ShiftScheduler
   from src.models import ShiftType
   from datetime import datetime
   
   scheduler = ShiftScheduler()
   scheduler.add_employee("EMP001", "Li Ming")
   ```

2. Assign a morning shift:
   ```python
   date = datetime(2025, 1, 6)
   scheduler.assign_shift("EMP001", date, ShiftType.MORNING)
   ```

3. Assign an afternoon shift **on the same day**:
   ```python
   # This should raise ValidationError, but it doesn't!
   scheduler.assign_shift("EMP001", date, ShiftType.AFTERNOON)
   ```

4. **Expected**: `ValidationError` is raised
5. **Actual**: Second shift is successfully assigned (BUG!)

## Issue Details

See [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for:
- Detailed problem analysis
- Affected files and line numbers
- Fix strategy (without actual fix code)
- Impact assessment

## Testing

### Test Categories

1. **Same-Day Shift Tests** (`test_same_day_shifts.py`) - **Currently FAILING**
   - `test_morning_and_afternoon_same_day_should_fail`
   - `test_morning_and_night_same_day_should_fail`
   - `test_afternoon_and_night_same_day_should_fail`
   - `test_same_shift_type_same_day_should_also_fail`
   - `test_different_days_should_succeed` (this one passes)

2. **Other Validation Tests** (`test_continuous_days.py`) - **Currently PASSING**
   - Consecutive days validation
   - Weekly hours validation
   - Night shift rest validation

## Development Environment

- **Python**: 3.10+
- **OS**: Windows 11
- **Testing Framework**: pytest

## License

MIT License - This is a demonstration project for bug reproduction and testing practice.
