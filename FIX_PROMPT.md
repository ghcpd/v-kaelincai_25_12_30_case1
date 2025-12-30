# Task: Fix the Shift Scheduler Bug

## Objective

You are a software engineer tasked with debugging and fixing a shift scheduling system. The system has a functional bug where business rules are not being properly enforced. Your goal is to identify and fix the issue, then create a corrected version of the project in a new directory.

## Background

This is an employee shift scheduling system for a factory production line. The system manages work shifts with the following business rules:

### Business Rules (All Must Be Enforced)
1. ✅ Employees cannot work more than 6 consecutive days without rest
2. ✅ After a night shift (22:00-06:00), employees must rest at least 12 hours
3. ✅ Employees cannot exceed 48 hours of work per week
4. ❌ **Employees cannot have multiple shifts on the same day** (BROKEN!)

### Shift Types
- **Morning**: 06:00 - 14:00 (8 hours)
- **Afternoon**: 14:00 - 22:00 (8 hours)
- **Night**: 22:00 - 06:00 next day (8 hours)

## Current Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   ├── models.py          # Employee and Shift data models
│   ├── scheduler.py       # Main scheduling logic
│   └── validator.py       # Business rule validation
├── tests/
│   ├── __init__.py
│   ├── test_same_day_shifts.py      # Tests for same-day rule (FAILING)
│   └── test_continuous_days.py      # Tests for other rules
├── data/
│   └── sample_shifts.json
├── requirements.txt
├── README.md
└── KNOWN_ISSUE.md
```

## Problem Statement

When you run the tests, you will see failures indicating that:
- The system allows assigning multiple shifts to the same employee on the same day
- This violates the business rule that states "one employee, one shift per day"

### How to Verify the Problem

Run these commands in the `issue_project/` directory:
```bash
pip install -r requirements.txt
pytest -v
```

**Expected Results:**
- Several tests in `test_same_day_shifts.py` will FAIL
- Tests show that `ValidationError` should be raised but isn't
- Other validation rules work correctly

## Your Task

### Step 1: Investigate
1. Run the tests to identify which scenarios fail
2. Examine the codebase to understand the validation workflow
3. Trace the code execution from `scheduler.assign_shift()` through the validator
4. Identify why the same-day validation is not working

### Step 2: Fix the Bug
1. Locate the root cause of the validation failure
2. Make the minimal necessary changes to fix the issue
3. Ensure your fix doesn't break other validations

### Step 3: Create Fixed Version
Create a new directory called `issue_project_fixed/` with the corrected code:

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   ├── models.py          # Copy from original (no changes needed)
│   ├── scheduler.py       # Copy from original (no changes needed)
│   └── validator.py       # FIXED VERSION
├── tests/
│   ├── __init__.py
│   ├── test_same_day_shifts.py      # Copy from original
│   └── test_continuous_days.py      # Copy from original
├── requirements.txt       # Copy from original
├── README.md             # Updated to reflect that bugs are fixed
└── FIX_SUMMARY.md        # NEW: Your explanation of the fix
```

## Deliverables

### 1. Fixed Project Directory
Create `issue_project_fixed/` with all corrected files.

### 2. FIX_SUMMARY.md
Create a file documenting your fix with the following sections:

```markdown
# Fix Summary

## Bug Identified
- Describe what was wrong
- Which file(s) and area of code were affected

## Root Cause
- Explain why the bug existed
- What was the developer's mistake

## Solution Applied
- What changes did you make (describe the approach, not just code)
- Why this fix solves the problem

## Changes Made
- List all modified files
- Briefly describe what changed in each file

## Verification
- Confirm all tests now pass
- Any additional testing performed
```

### 3. Updated README.md
Update the README in the fixed version to:
- Remove references to the bug
- Indicate this is the corrected version
- Show that all tests pass

## Success Criteria

Your fix is successful when:
1. ✅ All tests in `pytest -v` pass (12/12 tests)
2. ✅ Same-day shift validation now works correctly
3. ✅ Other validation rules still work correctly
4. ✅ Minimal code changes (avoid over-engineering)
5. ✅ FIX_SUMMARY.md clearly explains the issue and solution

## Constraints

- **Do NOT modify test files** - they correctly describe the expected behavior
- **Minimal changes** - fix only what's necessary
- **No external dependencies** - use only pytest
- **Preserve existing functionality** - don't break working validations
- **Use relative paths** - no absolute paths in any files

## Testing Commands

After creating the fixed version:

```bash
cd issue_project_fixed
pip install -r requirements.txt
pytest -v
```

Expected output: `12 passed in X.XXs` (all green)

## Hints for Investigation

- Start by reading the test failures carefully
- Examine which validation methods exist in the validator
- Compare which methods are actually called vs. which ones exist
- The fix is likely very simple (possibly a single line)
- Look for gaps in the validation pipeline

## Good Luck!

Your goal is to demonstrate debugging skills by:
1. Identifying the problem through testing and code analysis
2. Understanding the root cause
3. Implementing a clean, minimal fix
4. Documenting your findings clearly

Remember: The best fix is the simplest one that solves the problem!
