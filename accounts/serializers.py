from rest_framework import serializers
from .models import MemberProfile, WeightLog, ExerciseLog, Payment, Exercise

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class WeightLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightLog
        fields = ['id', 'date', 'weight_kg']

class ExerciseLogSerializer(serializers.ModelSerializer):
    # We can nest the ExerciseSerializer to show the full exercise details
    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = ExerciseLog
        fields = ['id', 'date', 'exercise', 'sets', 'reps', 'weight_lifted_kg', 'duration_minutes']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount_paid', 'payment_date', 'month_paid_for']

class MemberProfileSerializer(serializers.ModelSerializer):
    # Nesting other serializers to provide a complete member profile in one API call
    weight_logs = WeightLogSerializer(many=True, read_only=True)
    exercise_logs = ExerciseLogSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = MemberProfile
        fields = [
            'user', 'full_name', 'date_of_birth', 'phone_number', 
            'initial_weight_kg', 'fees_per_month', 'one_time_deposit',
            'weight_logs', 'exercise_logs', 'payments'
        ]
        # The 'user' field is read-only because it shouldn't be changed via the API
        read_only_fields = ['user']
