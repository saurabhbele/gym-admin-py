from django.core.management.base import BaseCommand
from accounts.models import Exercise

class Command(BaseCommand):
    help = 'Populates the database with default gym exercises'

    def handle(self, *args, **kwargs):
        exercises = [
            {'name': 'Bench Press', 'body_part': 'chest'},
            {'name': 'Incline Dumbbell Press', 'body_part': 'chest'},
            {'name': 'Push-ups', 'body_part': 'chest'},
            {'name': 'Cable Crossovers', 'body_part': 'chest'},
            
            {'name': 'Lat Pulldown', 'body_part': 'back'},
            {'name': 'Barbell Row', 'body_part': 'back'},
            {'name': 'Deadlift', 'body_part': 'back'},
            {'name': 'Pull-ups', 'body_part': 'back'},
            
            {'name': 'Squats', 'body_part': 'legs'},
            {'name': 'Leg Press', 'body_part': 'legs'},
            {'name': 'Lunges', 'body_part': 'legs'},
            {'name': 'Calf Raises', 'body_part': 'legs'},
            {'name': 'Leg Extensions', 'body_part': 'legs'},
            
            {'name': 'Overhead Press', 'body_part': 'shoulders'},
            {'name': 'Lateral Raises', 'body_part': 'shoulders'},
            {'name': 'Front Raises', 'body_part': 'shoulders'},
            
            {'name': 'Bicep Curls', 'body_part': 'biceps'},
            {'name': 'Hammer Curls', 'body_part': 'biceps'},
            {'name': 'Preacher Curls', 'body_part': 'biceps'},
            
            {'name': 'Tricep Extensions', 'body_part': 'triceps'},
            {'name': 'Skull Crushers', 'body_part': 'triceps'},
            {'name': 'Tricep Dips', 'body_part': 'triceps'},
            
            {'name': 'Crunches', 'body_part': 'core'},
            {'name': 'Plank', 'body_part': 'core'},
            {'name': 'Leg Raises', 'body_part': 'core'},
            
            {'name': 'Treadmill', 'body_part': 'cardio'},
            {'name': 'Stationary Bike', 'body_part': 'cardio'},
            {'name': 'Rowing Machine', 'body_part': 'cardio'},
            {'name': 'Stair Climber', 'body_part': 'cardio'}
        ]

        count = 0
        for ex in exercises:
            obj, created = Exercise.objects.get_or_create(
                name=ex['name'],
                defaults={'body_part': ex['body_part']}
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} default exercises to the database!'))
