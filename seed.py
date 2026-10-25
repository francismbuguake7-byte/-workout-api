
from datetime import date

from app import app
from server.models import Exercise, Workout, WorkoutExercise, db


def run():
    with app.app_context():
        db.create_all()

        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        db.session.commit()

        squat = Exercise(name='Squat', category='strength', equipment_needed=True)
        running = Exercise(name='Running', category='cardio', equipment_needed=False)
        stretch = Exercise(name='Hamstring Stretch', category='flexibility', equipment_needed=False)
        db.session.add_all([squat, running, stretch])

        leg_day = Workout(date=date(2026, 1, 10), duration_minutes=45, notes='Leg day')
        cardio = Workout(date=date(2026, 1, 12), duration_minutes=30, notes='Cardio session')
        db.session.add_all([leg_day, cardio])
        db.session.commit()

        db.session.add_all([
            WorkoutExercise(workout=leg_day, exercise=squat, reps=10, sets=4),
            WorkoutExercise(workout=leg_day, exercise=stretch, duration_seconds=60),
            WorkoutExercise(workout=cardio, exercise=running, duration_seconds=1200),
        ])
        db.session.commit()
        print('Database seeded.')


if __name__ == '__main__':
    run()
