from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from django.contrib.auth.models import User
from accounts.models import MemberProfile
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Creates an admin user for a specific tenant schema'

    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, help='The schema name of the tenant (e.g., gym_001)')
        parser.add_argument('username', type=str, help='The username for the new admin')
        parser.add_argument('password', type=str, help='The password for the new admin')

    def handle(self, *args, **kwargs):
        schema_name = kwargs['schema_name']
        username = kwargs['username']
        password = kwargs['password']

        try:
            with schema_context(schema_name):
                # 1. Create the User object
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={'email': f'{username}@{schema_name}.com', 'is_staff': True, 'is_superuser': True}
                )
                
                if not created:
                    self.stdout.write(self.style.WARNING(f"User '{username}' already exists. Updating password and permissions."))
                    user.is_staff = True
                    user.is_superuser = True
                
                user.set_password(password)
                user.save()

                # 2. Create the MemberProfile object so they can access the dashboard
                profile, profile_created = MemberProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'full_name': f"Admin ({username})",
                        'phone_number': f"admin-{user.id}", 
                        'fees_per_month': 0.00,
                        'is_admin': True,
                        'has_changed_password': True # So they aren't forced to change it immediately
                    }
                )

                self.stdout.write(self.style.SUCCESS(f"Successfully created/updated admin user '{username}' for tenant '{schema_name}'!"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating admin: {e}"))
            self.stdout.write(self.style.WARNING("Make sure you spelled the schema_name correctly!"))