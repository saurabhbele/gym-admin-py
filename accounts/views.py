from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import MemberProfile, WeightLog, Payment, ExerciseLog, Exercise, Attendance
from .forms import MemberProfileForm, WeightLogForm, ExerciseLogForm, UserForm, AttendanceForm, PaymentForm
from datetime import date

def dashboard(request):
    """
    The main dashboard view. It lists all gym members and calculates payment status.
    """
    members = MemberProfile.objects.all()
    
    # Calculate current month's first day
    today = date.today()
    current_month_start = date(today.year, today.month, 1)

    member_data = []
    for member in members:
        # Check if a payment exists for the current month
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

def member_detail(request, user_id):
    """
    Displays a detailed view of a single member's profile and activities.
    """
    member = get_object_or_404(MemberProfile, user_id=user_id)
    weight_logs = WeightLog.objects.filter(member=member).order_by('-date')
    payments = Payment.objects.filter(member=member).order_by('-month_paid_for')
    exercise_logs = ExerciseLog.objects.filter(member=member).order_by('-date')
    attendances = Attendance.objects.filter(member=member).order_by('-date')
    exercises = Exercise.objects.all()
    
    # Instantiate forms for adding new logs
    weight_form = WeightLogForm()
    exercise_form = ExerciseLogForm()
    attendance_form = AttendanceForm()
    payment_form = PaymentForm()

    context = {
        'member': member,
        'weight_logs': weight_logs,
        'payments': payments,
        'exercise_logs': exercise_logs,
        'attendances': attendances,
        'exercises': exercises,
        'weight_form': weight_form,
        'exercise_form': exercise_form,
        'attendance_form': attendance_form,
        'payment_form': payment_form,
    }
    return render(request, 'accounts/member_detail.html', context)

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
            return redirect('dashboard')
    else:
        user_form = UserForm()
        profile_form = MemberProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/add_member.html', context)


def edit_member(request, user_id):
    """
    Handles editing a member's profile.
    """
    member = get_object_or_404(MemberProfile, user_id=user_id)
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_detail', user_id=user_id)
    else:
        form = MemberProfileForm(instance=member)

    context = {
        'form': form,
        'member': member
    }
    return render(request, 'accounts/member_edit.html', context)

def edit_weight_log(request, log_id):
    """
    Handles editing a single weight log entry.
    """
    log = get_object_or_404(WeightLog, id=log_id)
    member = log.member
    if request.method == 'POST':
        form = WeightLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('member_detail', user_id=member.user.id)
    else:
        form = WeightLogForm(instance=log)

    context = {
        'form': form,
        'member': member
    }
    return render(request, 'accounts/log_edit.html', context)

def edit_exercise_log(request, log_id):
    """
    Handles editing a single exercise log entry.
    """
    log = get_object_or_404(ExerciseLog, id=log_id)
    member = log.member
    if request.method == 'POST':
        form = ExerciseLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('member_detail', user_id=member.user.id)
    else:
        form = ExerciseLogForm(instance=log)

    context = {
        'form': form,
        'member': member
    }
    return render(request, 'accounts/log_edit.html', context)

def add_weight_log(request, user_id):
    member = get_object_or_404(MemberProfile, user_id=user_id)
    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.member = member
            log.save()
    return redirect('member_detail', user_id=user_id)

def add_exercise_log(request, user_id):
    member = get_object_or_404(MemberProfile, user_id=user_id)
    if request.method == 'POST':
        form = ExerciseLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.member = member
            log.save()
    return redirect('member_detail', user_id=user_id)

def add_attendance(request, user_id):
    member = get_object_or_404(MemberProfile, user_id=user_id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.member = member
            log.save()
    return redirect('member_detail', user_id=user_id)

def add_payment(request, user_id):
    member = get_object_or_404(MemberProfile, user_id=user_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.member = member
            log.save()
    return redirect('member_detail', user_id=user_id)
