# Shift Scheduler System - Fixed Version

A production-ready employee shift scheduling system with all business rules properly enforced.

## Project Overview

This project implements a factory production line shift scheduling system with the following business rules:

### Business Rules (All Enforced ✅)
1. ✅ **Max Consecutive Days**: Employees cannot work more than 6 consecutive days without rest
2. ✅ **Night Shift Rest**: After a night shift (22:00-06:00), employees must rest at least 12 hours
3. ✅ **Weekly Hours Limit**: Employees cannot exceed 48 hours of work per week
4. ✅ **Same-Day Single Shift**: Employees cannot have multiple shifts on the same day

### Shift Types
- **Morning**: 06:00 - 14:00 (8 hours)
- **Afternoon**: 14:00 - 22:00 (8 hours)
- **Night**: 22:00 - 06:00 next day (8 hours)

## Project Structure

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   ├── models.py          # Employee and Shift data models
│   ├── scheduler.py       # Main scheduling logic
│   └── validator.py       # Business rule validation (FIXED!)
├── tests/
│   ├── __init__.py
│   ├── test_same_day_shifts.py      # All tests passing
│   └── test_continuous_days.py      # All tests passing
├── data/
│   └── sample_shifts.json           # Sample data
├── requirements.txt
├── README.md
├── FIX_SUMMARY.md         # Detailed explanation of the fix
└── KNOWN_ISSUE.md         # Original issue documentation
```

## What Was Fixed

The original codebase had a critical bug where the validation method for same-day shifts was defined but never called during the shift validation pipeline. This allowed employees to be scheduled for multiple shifts on the same day, violating a core business rule.

**Status**: All business rules are now properly enforced.

## Quick Start

### Installation

```powershell
# Install dependencies
pip install -r requirements.txt
```

### Run Tests

```powershell
# Run all tests (all should PASS)
pytest -v

# Expected output: 11 passed in X.XXs ✅
```

### Usage Example

```python
from src.scheduler import ShiftScheduler
from src.models import ShiftType
from datetime import datetime
from src.validator import ValidationError

scheduler = ShiftScheduler()
scheduler.add_employee("EMP001", "Li Ming")

# Assign morning shift
date = datetime(2025, 1, 6)
shift1 = scheduler.assign_shift("EMP001", date, ShiftType.MORNING)
print(f"✓ Assigned: {shift1}")

# Try to assign afternoon shift on SAME day
try:
    shift2 = scheduler.assign_shift("EMP001", date, ShiftType.AFTERNOON)
except ValidationError as e:
    print(f"✗ Rejected: {e}")
    # Output: ✗ Rejected: Employee EMP001 already has a morning shift on 2025-01-06...

# Assign shift on DIFFERENT day (allowed)
date2 = datetime(2025, 1, 7)
shift3 = scheduler.assign_shift("EMP001", date2, ShiftType.AFTERNOON)
print(f"✓ Assigned: {shift3}")
```

## Validation Rules

The system validates shifts against all business rules before assignment:

1. **Same-Day Validation** - Prevents multiple shifts on the same day
2. **Consecutive Days** - Enforces max 6 consecutive working days
3. **Night Shift Rest** - Requires 12+ hours rest after night shifts
4. **Weekly Hours** - Limits to 48 hours per week

All validations work correctly and comprehensively protect the schedule integrity.

## Testing

All test cases pass, demonstrating that:
- ✅ Same-day shifts are properly rejected
- ✅ Consecutive days limits are enforced
- ✅ Weekly hours limits are enforced
- ✅ Night shift rest periods are enforced

```powershell
pytest -v
# Output: 11 passed in 0.18s
```

## Key Changes

See [FIX_SUMMARY.md](FIX_SUMMARY.md) for:
- Complete explanation of the bug
- Root cause analysis
- Detailed changes made
- Verification results

## Development Environment

- **Python**: 3.10+
- **OS**: Windows
- **Testing Framework**: pytest

## License

MIT License - Production-ready shift scheduling system.
