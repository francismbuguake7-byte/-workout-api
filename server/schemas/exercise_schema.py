from marshmallow import (Schema, ValidationError, fields, validate,
                        validates)

CATEGORIES = ['strength', 'cardio', 'flexibility', 'balance']


class ExerciseSchema(Schema):
    """Serialize/deserialize Exercise records."""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True,
                      validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True,
                          validate=validate.OneOf(CATEGORIES))
    equipment_needed = fields.Bool(load_default=False)
    # Associated workouts (via the join rows) when showing one exercise.
    workout_exercises = fields.Nested(
        'WorkoutExerciseSchema', many=True, dump_only=True,
        exclude=('exercise',))

    @validates('name')
    def validate_name(self, value, **kwargs):
        """Schema validation: reject blank/whitespace names."""
        if not value.strip():
            raise ValidationError('Name cannot be blank.')
