from datetime import date

from marshmallow import (Schema, ValidationError, fields, validate,
                        validates)


class WorkoutSchema(Schema):
    

    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)
  
    workout_exercises = fields.Nested(
        'WorkoutExerciseSchema', many=True, dump_only=True,
        exclude=('workout',))

    @validates('date')
    def validate_date(self, value, **kwargs):
      
        if value > date.today():
            raise ValidationError('Date cannot be in the future.')
