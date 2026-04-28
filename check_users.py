import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_site.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import MemberProfile

users = User.objects.all()
for u in users:
    try:
        profile = u.member_profile
        print(f"User: {u.username}, Profile: {profile.full_name}")
    except MemberProfile.DoesNotExist:
        print(f"User: {u.username}, NO PROFILE")
