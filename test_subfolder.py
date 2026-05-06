import inspect
import sys
import os

try:
    import django_tenants.middleware.subfolder
    print(inspect.getsource(django_tenants.middleware.subfolder.TenantSubfolderMiddleware))
except Exception as e:
    print(e)
