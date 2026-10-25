from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


from server.models.exercise import Exercise
from server.models.workout import Workout
from server.models.workout_exercise import WorkoutExercise
