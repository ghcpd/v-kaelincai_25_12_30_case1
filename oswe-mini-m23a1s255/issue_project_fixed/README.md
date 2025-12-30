# Shift Scheduler System — Fixed

This is the corrected version of the shift scheduler kata. The bug that allowed
assigning multiple shifts to the same employee on the same day has been fixed.

Status: all tests pass (see verification below).

Business rules enforced:
- Employees cannot work more than 6 consecutive days without rest
- After a night shift (22:00-06:00), employees must rest at least 12 hours
- Employees cannot exceed 48 hours of work per week
- Employees cannot have multiple shifts on the same day (fixed)

Quick verification

```powershell
pip install -r requirements.txt
pytest -q
# Expected: 12 passed
```
