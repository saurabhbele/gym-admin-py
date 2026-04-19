from django.contrib import admin
from .models import (
    MemberProfile, 
    Attendance, 
    WeightLog, 
    Exercise, 
    ExerciseLog, 
    Payment
)

# To make the admin interface more user-friendly, we can customize how models are displayed.

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'is_admin', 'fees_per_month')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('is_admin',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'present')
    list_filter = ('date', 'present')
    search_fields = ('member__full_name',)

@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'weight_kg')
    list_filter = ('date',)
    search_fields = ('member__full_name',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'body_part')
    list_filter = ('body_part',)
    search_fields = ('name',)

@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'exercise', 'sets', 'reps', 'weight_lifted_kg')
    list_filter = ('date', 'exercise__body_part')
    search_fields = ('member__full_name', 'exercise__name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'payment_date', 'amount_paid', 'month_paid_for')
    list_filter = ('payment_date', 'month_paid_for')
    search_fields = ('member__full_name',)
