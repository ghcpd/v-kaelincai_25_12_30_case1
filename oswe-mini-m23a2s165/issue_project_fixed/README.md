# Shift Scheduler System — Fixed Version

This repository contains the fixed version of the Shift Scheduler System. The bug preventing enforcement of the "one shift per employee per day" rule has been corrected.

## What changed
- The validator now enforces the same-day single-shift rule.
- All tests pass (including same-day validations).

## How to run

pip install -r requirements.txt
pytest -v
