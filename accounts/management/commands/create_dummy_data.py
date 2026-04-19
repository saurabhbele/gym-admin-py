import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import MemberProfile, WeightLog, Payment, Exercise, ExerciseLog

class Command(BaseCommand):
    help = 'Creates dummy data for the gym application'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        # Clear existing data to prevent duplicates
        User.objects.exclude(is_superuser=True).delete()
        MemberProfile.objects.all().delete()
        WeightLog.objects.all().delete()
        Payment.objects.all().delete()
        Exercise.objects.all().delete()
        ExerciseLog.objects.all().delete()

        self.stdout.write("Creating new data...")

        # Create some default exercises
        exercises_data = [
            {'name': 'Bench Press', 'body_part': 'chest'},
            {'name': 'Squat', 'body_part': 'legs'},
            {'name': 'Deadlift', 'body_part': 'back'},
            {'name': 'Overhead Press', 'body_part': 'shoulders'},
            {'name': 'Bicep Curl', 'body_part': 'biceps'},
            {'name': 'Tricep Extension', 'body_part': 'triceps'},
            {'name': 'Treadmill Run', 'body_part': 'cardio'},
        ]
        for ex_data in exercises_data:
            Exercise.objects.get_or_create(**ex_data)
        
        all_exercises = list(Exercise.objects.all())

        first_names = ['John', 'Jane', 'Peter', 'Emily', 'Michael']
        last_names = ['Smith', 'Doe', 'Jones', 'Williams', 'Brown']
        
        for i in range(5):
            # 1. Create a User
            username = f'member{i+1}'
            first_name = first_names[i]
            last_name = last_names[i]
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'first_name': first_name, 'last_name': last_name, 'email': f'{username}@example.com'}
            )
            user.set_password('password')
            user.save()

            # 2. Create a MemberProfile
            member = MemberProfile.objects.create(
                user=user,
                full_name=f'{first_name} {last_name}',
                phone_number=f'555-010{i}',
                date_of_birth=date(1990 + i, 1, 1),
                initial_weight_kg=random.uniform(60.0, 90.0),
                fees_per_month=random.choice([50.00, 75.00, 100.00]),
                one_time_deposit=200.00,
            )

            # 3. Create weekly WeightLog for the past 4 weeks
            current_weight = member.initial_weight_kg
            for week in range(4, 0, -1):
                log_date = date.today() - timedelta(weeks=week)
                WeightLog.objects.create(
                    member=member,
                    date=log_date,
                    weight_kg=round(current_weight - random.uniform(0.2, 0.5), 2)
                )
                current_weight -= random.uniform(0.2, 0.5)

                # Create a couple of exercise logs for that day
                for _ in range(2):
                    ExerciseLog.objects.create(
                        member=member,
                        date=log_date,
                        exercise=random.choice(all_exercises),
                        sets=random.randint(3, 5),
                        reps=random.randint(8, 12),
                        weight_lifted_kg=random.uniform(20, 100)
                    )

            # 4. Create Payments for the last 3 months
            for month_offset in range(3, 0, -1):
                current_date = date.today()
                target_month = current_date.month - month_offset
                target_year = current_date.year
                while target_month <= 0:
                    target_month += 12
                    target_year -= 1
                payment_month_start = date(target_year, target_month, 1)

                if i == 4 and month_offset == 1:
                    continue
                
                Payment.objects.create(
                    member=member,
                    amount_paid=member.fees_per_month,
                    payment_date=payment_month_start,
                    month_paid_for=payment_month_start
                )

        self.stdout.write(self.style.SUCCESS('Successfully created dummy data!'))
