from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


from models.exercise import Exercise  
from models.workout import Workout  
from models.workout_exercise import WorkoutExercise 
