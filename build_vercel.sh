#!/bin/bash

# Vercel uses Amazon Linux. We need to tell pip to use --user or a venv if PEP 668 is active.
# The easiest way on Vercel is to just run collectstatic and migrations during the build step.
# Vercel's Python builder handles the dependency installation automatically via requirements.txt.

python3.9 manage.py collectstatic --no-input
python3.9 manage.py migrate
