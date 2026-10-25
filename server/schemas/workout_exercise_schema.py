from marshmallow import Schema, fields, validate


class WorkoutExerciseSchema(Schema):
   

    id = fields.Int(dump_only=True)
    workout_id = fields.Int()
    exercise_id = fields.Int()
    reps = fields.Int(validate=validate.Range(min=0), allow_none=True)
    sets = fields.Int(validate=validate.Range(min=0), allow_none=True)
    duration_seconds = fields.Int(
        validate=validate.Range(min=0), allow_none=True)
    exercise = fields.Nested(
        'ExerciseSchema', only=('id', 'name', 'category'), dump_only=True)
    workout = fields.Nested(
        'WorkoutSchema', only=('id', 'date', 'duration_minutes'),
        dump_only=True)
