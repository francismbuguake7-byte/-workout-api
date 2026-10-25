from flask import Blueprint, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models import Exercise, Workout, WorkoutExercise, db
from schemas import WorkoutExerciseSchema

we_bp = Blueprint('workout_exercises', __name__)
schema = WorkoutExerciseSchema()
many_schema = WorkoutExerciseSchema(many=True)
def save_or_rollback():
    try:
        db.session.commit()
        return None
    except IntegrityError:
        db.session.rollback()
        return {'error': 'The record conflicts with existing data.'}, 409
    except SQLAlchemyError:
        db.session.rollback()
        return {'error': 'Database operation failed.'}, 500


@we_bp.get('/workout_exercises')
def list_workout_exercises():
    records = WorkoutExercise.query.order_by(WorkoutExercise.id).all()
    return many_schema.dump(records), 200


@we_bp.get('/workout_exercises/<int:id>')
def get_workout_exercise(id):
    record = db.session.get(WorkoutExercise, id)
    if record is None:
        return {'error': 'Workout exercise not found'}, 404
    return schema.dump(record), 200


@we_bp.post('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises')
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if workout is None or exercise is None:
        return {'error': 'Workout or exercise not found'}, 404
    payload = request.get_json(silent=True)
    if payload is None:
        payload = {}
    if not isinstance(payload, dict):
        return {'error': 'Request body must be a JSON object.'}, 400
    payload['workout_id'] = workout_id
    payload['exercise_id'] = exercise_id
    try:
        data = schema.load(payload)
        record = WorkoutExercise(**data)
        db.session.add(record)
    except ValidationError as err:
        return {'errors': err.messages}, 422
    except (TypeError, ValueError) as err:
        db.session.rollback()
        return {'error': str(err)}, 422
    error = save_or_rollback()
    if error:
        return error
    return schema.dump(record), 201


@we_bp.route('/workout_exercises/<int:id>', methods=['PUT', 'PATCH'])
def update_workout_exercise(id):
    record = db.session.get(WorkoutExercise, id)
    if record is None:
        return {'error': 'Workout exercise not found'}, 404
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return {'error': 'Request body must be a JSON object.'}, 400
    try:
        data = schema.load(payload, partial=request.method == 'PATCH')
        for key, value in data.items():
            if key in {'workout_id', 'exercise_id'}:
                related_model = Workout if key == 'workout_id' else Exercise
                if db.session.get(related_model, value) is None:
                    return {'error': f'{key} does not reference an existing record.'}, 404
            setattr(record, key, value)
    except ValidationError as err:
        return {'errors': err.messages}, 422
    except (TypeError, ValueError) as err:
        db.session.rollback()
        return {'error': str(err)}, 422
    error = save_or_rollback()
    if error:
        return error
    return schema.dump(record), 200


@we_bp.delete('/workout_exercises/<int:id>')
def delete_workout_exercise(id):
    record = db.session.get(WorkoutExercise, id)
    if record is None:
        return {'error': 'Workout exercise not found'}, 404
    db.session.delete(record)
    error = save_or_rollback()
    if error:
        return error
    return '', 204
