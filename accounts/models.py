from django.db import models
from django.contrib.auth.models import User

# It's good practice to define a custom user model if you anticipate
# adding fields directly to the user for authentication purposes.
# For now, we'll link MemberProfile to Django's default User model.
# If you later decide to replace Django's User model, you would set AUTH_USER_MODEL in settings.py
# and potentially define a CustomUser class inheriting from a different base class.

class MemberProfile(models.Model):
    """
    Stores core information about each gym member.
    Links to Django's built-in User model for authentication.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='member_profile')
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    initial_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # Initial weight in kg

    # Financials
    fees_per_month = models.DecimalField(max_digits=8, decimal_places=2)
    one_time_deposit = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # To distinguish admin from regular members.
    # Note: For robust admin roles, consider Django's built-in permissions/groups or user.is_staff.
    is_admin = models.BooleanField(default=False) 

    has_changed_password = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

class Attendance(models.Model):
    """
    Records daily attendance for members.
    """
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    present = models.BooleanField(default=True)

    class Meta:
        unique_together = ('member', 'date') # A member can only have one attendance record per day
        ordering = ['-date'] # Order by most recent attendance first

    def __str__(self):
        return f"{self.member.full_name} - {self.date} - {'Present' if self.present else 'Absent'}"

class WeightLog(models.Model):
    """
    Records weekly (or daily) weight checks for members.
    """
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='weight_logs')
    date = models.DateField()
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2) # Weight in kg

    class Meta:
        unique_together = ('member', 'date') # A member can only have one weight log per day
        ordering = ['-date']

    def __str__(self):
        return f"{self.member.full_name} - {self.date}: {self.weight_kg} kg"

class Exercise(models.Model):
    """
    A lookup table for different types of exercises.
    """
    name = models.CharField(max_length=100, unique=True) # e.g., 'Chest Press', 'Squats', 'Bicep Curls'
    body_part = models.CharField(
        max_length=50, 
        choices=[
            ('chest', 'Chest'), ('back', 'Back'), ('legs', 'Legs'), 
            ('shoulders', 'Shoulders'), ('biceps', 'Biceps'), ('triceps', 'Triceps'),
            ('core', 'Core'), ('cardio', 'Cardio'), ('other', 'Other')
        ],
        blank=True, null=True
    )

    def __str__(self):
        return self.name

class ExerciseLog(models.Model):
    """
    Records the exercises a member performed on a specific date.
    """
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='exercise_logs')
    date = models.DateField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    weight_lifted_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True) # Weight lifted in kg
    duration_minutes = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date', 'exercise__name'] # Order by most recent date, then exercise name

    def __str__(self):
        return f"{self.member.full_name} - {self.date} - {self.exercise.name}"

class Payment(models.Model):
    """
    Tracks fee and deposit payments made by members.
    """
    PAYMENT_TYPE_CHOICES = [
        ('Monthly Fee', 'Monthly Fee'),
        ('Deposit', 'One-Time Deposit'),
        ('Other', 'Other')
    ]
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES, default='Monthly Fee')
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateField()
    # Stores the first day of the month for which the payment is made. Optional for deposits.
    month_paid_for = models.DateField(null=True, blank=True) 

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.member.full_name} - Paid {self.amount_paid} for {self.payment_type}"

class DietPlan(models.Model):
    """
    Stores a nutritional diet plan assigned to a specific member.
    """
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='diet_plans')
    date_assigned = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=150, help_text="E.g., 'Weight Loss Plan (April)'")
    breakfast = models.TextField(blank=True)
    lunch = models.TextField(blank=True)
    dinner = models.TextField(blank=True)
    snacks = models.TextField(blank=True)
    notes = models.TextField(blank=True, help_text="Additional instructions or guidelines.")

    class Meta:
        ordering = ['-date_assigned']

    def __str__(self):
        return f"{self.title} for {self.member.full_name}"
