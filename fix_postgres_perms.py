import os
import django
import psycopg2

print("""
The error "permission denied for schema public" happens because starting in PostgreSQL 15,
the default permissions for the 'public' schema were changed to be more secure. By default,
users no longer have permission to create tables in the 'public' schema unless they are the owner
of the database or the schema.

To fix this, you need to open your psql terminal again as a superuser (like 'postgres')
and grant the 'CREATE' permission on the 'public' schema to your 'gym_admin' user.

Please open your terminal and run:

    sudo -u postgres psql -d gym_saas

Then, run this exact SQL command:

    GRANT CREATE ON SCHEMA public TO gym_admin;
    \\q

After doing that, you should be able to run 'python manage.py migrate_schemas --shared' successfully.
""")