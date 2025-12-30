# Fix Summary

## Bug Identified
- The same-day shift validation existed but was never executed, allowing an
  employee to be assigned multiple shifts on the same calendar day.
- Affected file: `src/validator.py` (the method `_validate_same_day_shifts` was
  defined but not called).

## Root Cause
- Developer added a dedicated validation helper for the "one shift per day"
  rule but omitted the call in the `validate_new_shift` pipeline. As a result,
  the rule was never enforced even though the logic was present.

## Solution Applied
- Invoked the existing `_validate_same_day_shifts(new_shift)` from
  `validate_new_shift` so the check runs for every attempted assignment.
- Added a minimal, well-tested `src/models.py` implementation in the fixed
  workspace (the original exercise expected this model to be present).
- No other validation logic was changed.

## Changes Made
- Added: `src/models.py` (implement Employee, Shift, ShiftType)
- Fixed: `src/validator.py` (call `_validate_same_day_shifts` from the
  validation pipeline)
- Copied: `src/scheduler.py`, `tests/*`, `requirements.txt` into the fixed
  project
- Documentation: updated `README.md`, added this `FIX_SUMMARY.md`

## Verification
- Ran the full test-suite: `pytest -q` → **12 passed**
- Manual inspection: ensured the same-day rule triggers for all combinations
  (morning+afternoon, morning+night, afternoon+night, duplicate shift types)

## Notes
- Fix is minimal and backward compatible with existing behaviour and tests.
- No changes were made to test files.
