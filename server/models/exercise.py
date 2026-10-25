from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

from models import db

CATEGORIES = ['strength', 'cardio', 'flexibility', 'balance']


class Exercise(db.Model):
   

    __tablename__ = 'exercises'
    __table_args__ = (
       
        db.UniqueConstraint('name', name='uq_exercise_name'),
        db.CheckConstraint(
            "category IN ('strength','cardio','flexibility','balance')",
            name='ck_exercise_category'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise',
        cascade='all, delete-orphan')
  
    workouts = association_proxy('workout_exercises', 'workout')

    @validates('name')
    def validate_name(self, key, value):
       
        if not value or not value.strip():
            raise ValueError('Exercise name is required.')
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
       
        if value not in CATEGORIES:
            raise ValueError(f'Category must be one of {CATEGORIES}.')
        return value

    def __repr__(self):
        return f'<Exercise {self.id} {self.name}>'
