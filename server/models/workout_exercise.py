from sqlalchemy.orm import validates

from server.models import db


class WorkoutExercise(db.Model):
    

    __tablename__ = 'workout_exercises'
    __table_args__ = (
        
        db.CheckConstraint('reps >= 0', name='ck_we_reps'),
        db.CheckConstraint('sets >= 0', name='ck_we_sets'),
        db.CheckConstraint('duration_seconds >= 0', name='ck_we_duration'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(
        db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps', 'sets', 'duration_seconds')
    def validate_non_negative(self, key, value):
      
        if value is not None and value < 0:
            raise ValueError(f'{key} cannot be negative.')
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}>'
