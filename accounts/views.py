import csv
from io import TextIOWrapper
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import MemberProfile, WeightLog, Payment, ExerciseLog, Exercise, Attendance, DietPlan
from .forms import MemberProfileForm, WeightLogForm, ExerciseLogForm, UserForm, AttendanceForm, PaymentForm, CSVImportForm, DietPlanForm
from datetime import date
from .utils import render_to_pdf # Custom utility for PDF generation

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
def dashboard(request):
    """
    The main dashboard view. 
    If admin: lists all gym members and calculates payment status.
    If regular user: redirects to their own profile.
    """
    if not request.user.is_staff:
        # Redirect regular users to their own profile page
        try:
            profile = request.user.member_profile
            
            # Require password change on first login
            if not profile.has_changed_password:
                messages.info(request, "Please change your password before continuing.")
                return redirect('change_password')

            return redirect('member_detail', user_id=request.user.id)
        except MemberProfile.DoesNotExist:
            messages.error(request, "Your profile is not fully set up. Please contact an administrator.")
            return redirect('change_password') # Best to redirect them somewhere safe like change password

    # Admin view logic
    members = MemberProfile.objects.all()
    
    today = date.today()
    current_month_start = date(today.year, today.month, 1)

    member_data = []
    for member in members:
        has_paid = Payment.objects.filter(
            member=member, 
            month_paid_for=current_month_start
        ).exists()
        
        member_data.append({
            'profile': member,
            'has_paid_current_month': has_paid
        })

    context = {
        'member_data': member_data
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def member_detail(request, user_id):
    """
    Displays a detailed view of a single member's profile and activities.
    """
    # The member we want to view
    member = get_object_or_404(MemberProfile, user_id=user_id)
    
    # Security check: Ensure regular users can only see their own profile
    if not request.user.is_staff and request.user.id != member.user.id:
        messages.error(request, "You do not have permission to view this profile.")
        return redirect('dashboard')

    if not request.user.is_staff:
        try:
            profile = request.user.member_profile
            if not profile.has_changed_password:
                messages.info(request, "Please change your password before continuing.")
                return redirect('change_password')
        except MemberProfile.DoesNotExist:
            pass

    weight_logs = WeightLog.objects.filter(member=member).order_by('-date')
    payments = Payment.objects.filter(member=member).order_by('-month_paid_for')
    exercise_logs = ExerciseLog.objects.filter(member=member).order_by('-date')
    attendances = Attendance.objects.filter(member=member).order_by('-date')
    diet_plans = DietPlan.objects.filter(member=member).order_by('-date_assigned')
    exercises = Exercise.objects.all()
    
    weight_form = WeightLogForm()
    exercise_form = ExerciseLogForm()
    attendance_form = AttendanceForm()
    payment_form = PaymentForm()
    diet_form = DietPlanForm()

    context = {
        'member': member,
        'weight_logs': weight_logs,
        'payments': payments,
        'exercise_logs': exercise_logs,
        'attendances': attendances,
        'diet_plans': diet_plans,
        'exercises': exercises,
        'weight_form': weight_form,
        'exercise_form': exercise_form,
        'attendance_form': attendance_form,
        'payment_form': payment_form,
        'diet_form': diet_form,
        'is_admin': request.user.is_staff, # Pass to template to hide/show edit buttons
    }
    return render(request, 'accounts/member_detail.html', context)

@user_passes_test(is_admin)
def add_member(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = MemberProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Member added successfully.")
            return redirect('dashboard')
    else:
        user_form = UserForm()
        profile_form = MemberProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/add_member.html', context)


@user_passes_test(is_admin)
def edit_member(request, user_id):
    member = get_object_or_404(MemberProfile, user_id=user_id)
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('member_detail', user_id=user_id)
    else:
        form = MemberProfileForm(instance=member)
    context = {'form': form, 'member': member}
    return render(request, 'accounts/member_edit.html', context)

@user_passes_test(is_admin)
def edit_weight_log(request, log_id):
    log = get_object_or_404(WeightLog, id=log_id)
    member = log.member
    if request.method == 'POST':
        form = WeightLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('member_detail', user_id=member.user.id)
    else:
        form = WeightLogForm(instance=log)
    context = {'form': form, 'member': member}
    return render(request, 'accounts/log_edit.html', context)

@user_passes_test(is_admin)
def edit_exercise_log(request, log_id):
    log = get_object_or_404(ExerciseLog, id=log_id)
    member = log.member
    if request.method == 'POST':
        form = ExerciseLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('member_detail', user_id=member.user.id)
    else:
        form = ExerciseLogForm(instance=log)
    context = {'form': form, 'member': member}
    return render(request, 'accounts/log_edit.html', context)

@user_passes_test(is_admin)
def add_weight_log(request, user_id):
    member = get_object_or_404(MemberProfile, user_id=user_id)
    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.member = member
            log.save()
            messages.success(request, "Weight logged.")
    return redirect('member_detail', user_id=user_id)

@user_passes_test(is_admin)
def add_exercise_log(request, user_id):
    member = get_object_or_404(MemberProfile, user_id=user_id)
    if request.method == 'POST':
        form = ExerciseLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.member = member
            log.save()
            messages.success(request, "Workout logged.")
    return redirect('member_detail', user_id=user_id)

@user_passes_test(is_admin)
def add_attendance(request, user_id):
    member = get_object_or_404(MemberProfile, user_id=user_id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.member = member
            log.save()
            messages.success(request, "Attendance logged.")
    return redirect('member_detail', user_id=user_id)

@user_passes_test(is_admin)
def add_payment(request, user_id):
    member = get_object_or_404(MemberProfile, user_id=user_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.member = member
            log.save()
            messages.success(request, "Payment logged.")
    return redirect('member_detail', user_id=user_id)

@user_passes_test(is_admin)
def add_diet_plan(request, user_id):
    member = get_object_or_404(MemberProfile, user_id=user_id)
    if request.method == 'POST':
        form = DietPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.member = member
            plan.save()
            messages.success(request, "Diet plan saved.")
    return redirect('member_detail', user_id=user_id)

@login_required
def change_password(request):
    """
    Allows a user to change their own password.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important, to update the session with the new password
            messages.success(request, 'Your password was successfully updated!')
            
            # Mark that they have changed their password
            try:
                profile = request.user.member_profile
                profile.has_changed_password = True
                profile.save()
            except MemberProfile.DoesNotExist:
                pass

            if request.user.is_staff:
                return redirect('dashboard')
            else:
                # Need to use the current user's ID
                return redirect('member_detail', user_id=request.user.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

@user_passes_test(is_admin)
def admin_reset_password(request, user_id):
    """
    Allows an admin to set a new password for any user.
    """
    user_to_change = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        # Instead of the normal PasswordChangeForm which requires old password,
        # we just set the new password directly from a simple POST form.
        new_password = request.POST.get('new_password')
        if new_password:
            user_to_change.set_password(new_password)
            user_to_change.save()
            
            profile = getattr(user_to_change, 'member_profile', None)
            if profile:
                profile.has_changed_password = False # Force them to change it again
                profile.save()

            messages.success(request, f'Password successfully reset for {user_to_change.username}.')
            return redirect('member_detail', user_id=user_id)
        else:
             messages.error(request, 'Password cannot be empty.')
    
    return render(request, 'accounts/admin_reset_password.html', {
        'user_to_change': user_to_change
    })

@user_passes_test(is_admin)
def import_members(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'This is not a CSV file.')
                return redirect('import_members')

            try:
                file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
                reader = csv.DictReader(file_data)
                
                success_count = 0
                error_count = 0
                
                for row in reader:
                    username = row.get('username')
                    email = row.get('email', '')
                    full_name = row.get('full_name', '')
                    phone_number = row.get('phone_number', '')
                    initial_weight_kg = row.get('initial_weight_kg')
                    fees_per_month = row.get('fees_per_month', 0.00)
                    
                    if not username or not full_name or not phone_number:
                        error_count += 1
                        continue
                        
                    # Parse numerical values carefully
                    try:
                        initial_weight_kg = float(initial_weight_kg) if initial_weight_kg else None
                        fees_per_month = float(fees_per_month)
                    except ValueError:
                        initial_weight_kg = None
                        fees_per_month = 0.00

                    # Check if user already exists
                    if User.objects.filter(username=username).exists():
                        error_count += 1
                        continue
                        
                    # Create User
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password='password123' # Default password, users will be forced to change it
                    )
                    
                    # Create Profile
                    MemberProfile.objects.create(
                        user=user,
                        full_name=full_name,
                        phone_number=phone_number,
                        initial_weight_kg=initial_weight_kg,
                        fees_per_month=fees_per_month,
                        has_changed_password=False # Forces them to change 'password123' on first login
                    )
                    success_count += 1
                    
                messages.success(request, f"Successfully imported {success_count} members. {error_count} failed or skipped.")
                return redirect('dashboard')
                
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
                return redirect('import_members')
    else:
        form = CSVImportForm()
        
    return render(request, 'accounts/import_members.html', {'form': form})

@login_required
def generate_member_pdf(request, user_id):
    """
    Generates a PDF report for a specific member.
    Accessible by the admin or the member themselves.
    """
    member = get_object_or_404(MemberProfile, user_id=user_id)
    
    # Security check
    if not request.user.is_staff and request.user.id != member.user.id:
        messages.error(request, "You do not have permission to view this report.")
        return redirect('dashboard')

    # Get data for the report (e.g., last 30 days, or just all for simplicity)
    weight_logs = WeightLog.objects.filter(member=member).order_by('-date')[:10]
    payments = Payment.objects.filter(member=member).order_by('-payment_date')[:5]
    exercise_logs = ExerciseLog.objects.filter(member=member).order_by('-date')[:20]
    attendances = Attendance.objects.filter(member=member).order_by('-date')[:30]

    context = {
        'member': member,
        'weight_logs': weight_logs,
        'payments': payments,
        'exercise_logs': exercise_logs,
        'attendances': attendances,
        'today': date.today(),
    }
    
    pdf = render_to_pdf('accounts/pdf_report.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Report_{member.full_name.replace(' ', '_')}_{date.today()}.pdf"
        # Uncomment the line below to force download instead of viewing in browser
        # response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
    
    messages.error(request, "Error generating PDF report.")
    return redirect('member_detail', user_id=user_id)
