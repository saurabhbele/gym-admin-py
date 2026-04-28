from django.shortcuts import render, redirect
from django.contrib import messages
from django_tenants.utils import schema_context
from django.contrib.auth.models import User
from accounts.models import MemberProfile
from .forms import TenantForm
from .models import Client, Domain

def public_home(request):
    """
    This is the main landing page for your SaaS platform (e.g., gymsaas.com).
    It handles registering new gyms (tenants).
    """
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            try:
                # 1. Create the tenant (This automatically creates the PostgreSQL schema!)
                tenant = form.save(commit=False)
                tenant.save()

                # 2. Link a domain to the tenant
                domain_url = form.cleaned_data['domain_url']
                Domain.objects.create(
                    domain=domain_url,
                    tenant=tenant,
                    is_primary=True
                )
                
                # 3. Provision the initial admin user inside the new tenant schema
                admin_user = form.cleaned_data['admin_username']
                admin_pass = form.cleaned_data['admin_password']
                
                # Switch the database context to the newly created schema
                with schema_context(tenant.schema_name):
                    user = User.objects.create_user(
                        username=admin_user, 
                        password=admin_pass, 
                        is_staff=True, 
                        is_superuser=True
                    )
                    
                    MemberProfile.objects.create(
                        user=user,
                        full_name=f"Admin ({admin_user})",
                        phone_number=f"admin-{user.id}", 
                        fees_per_month=0.00,
                        is_admin=True,
                        has_changed_password=True # Don't force password change
                    )

                messages.success(request, f"Successfully created new gym schema: {tenant.name}! You can now visit http://{domain_url}:8000 and login with '{admin_user}'.")
                return redirect('public_home')
                
            except Exception as e:
                # Catching schema creation errors (e.g., schema name already exists)
                messages.error(request, f"Error creating gym: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TenantForm()
    
    # Exclude the 'public' tenant from the list of client gyms
    tenants = Client.objects.exclude(schema_name='public')
    
    return render(request, 'clients/public_home.html', {
        'form': form, 
        'tenants': tenants
    })
