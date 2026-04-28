from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import MemberProfile

class Command(BaseCommand):
    help = 'Creates missing MemberProfiles for ALL users created manually'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        count = 0
        for user in users:
            try:
                profile = getattr(user, 'member_profile')
                if not profile:
                    raise MemberProfile.DoesNotExist
            except MemberProfile.DoesNotExist:
                MemberProfile.objects.create(
                    user=user,
                    full_name=user.get_full_name() or user.username,
                    phone_number=f"pending-{user.id}",
                    fees_per_month=0.00,
                    is_admin=user.is_staff
                )
                self.stdout.write(self.style.SUCCESS(f"Created missing profile for user: {user.username} (Staff: {user.is_staff})"))
                count += 1
            
        if count == 0:
            self.stdout.write("No missing profiles found.")
        else:
            self.stdout.write(self.style.SUCCESS(f"Successfully fixed {count} users!"))
