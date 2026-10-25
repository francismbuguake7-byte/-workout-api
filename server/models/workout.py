from datetime import date as date_cls

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

from models import db


class Workout(db.Model):
   

    __tablename__ = 'workouts'
    __table_args__ = (
        
        db.CheckConstraint('duration_minutes > 0', name='ck_workout_duration'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout',
        cascade='all, delete-orphan')
   
    exercises = association_proxy('workout_exercises', 'exercise')

    @validates('duration_minutes')
    def validate_duration(self, key, value):
       
        if value is None or value <= 0:
            raise ValueError('duration_minutes must be positive.')
        return value

    @validates('date')
    def validate_date(self, key, value):
      
        if value and value > date_cls.today():
            raise ValueError('Workout date cannot be in the future.')
        return value

    def __repr__(self):
        return f'<Workout {self.id} {self.date}>'
