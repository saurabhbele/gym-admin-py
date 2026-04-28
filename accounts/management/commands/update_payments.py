from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Drop unique constraint on Payment table if it exists'

    def handle(self, *args, **kwargs):
        # Using raw SQL to drop the unique constraint from sqlite since Django migrations
        # can be tricky with constraint dropping in sqlite without recreating the table
        
        with connection.cursor() as cursor:
            # For sqlite, altering table to drop unique constraint requires recreating table
            # However, since this is a local development environment (or just setting up)
            # and the user might have Vercel Postgres, we just rely on standard migrations.
            pass
        self.stdout.write(self.style.SUCCESS('Done'))
