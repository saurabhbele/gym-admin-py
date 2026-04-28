#!/bin/bash
# exit on error
set -o errexit

pip install --break-system-packages -r requirements.txt
python manage.py collectstatic --no-input

# 1. Migrate the shared/public tables first (like the Domains and Clients list)
python manage.py migrate_schemas --shared

# 2. Migrate ALL tenant schemas automatically
python manage.py migrate_schemas --tenant
