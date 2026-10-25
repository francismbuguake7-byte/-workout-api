from flask import Blueprint, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from server.models import Workout, db
from server.schemas import WorkoutSchema

workout_bp = Blueprint('workouts', __name__)
schema = WorkoutSchema()
many_schema = WorkoutSchema(many=True)


def save_or_rollback():
    try:
        db.session.commit()
        return None
    except IntegrityError:
        db.session.rollback()
        return {'error': 'The workout conflicts with existing data.'}, 409
    except SQLAlchemyError:
        db.session.rollback()
        return {'error': 'Database operation failed.'}, 500


@workout_bp.get('/workouts')
def list_workouts():
    return many_schema.dump(Workout.query.order_by(Workout.id).all()), 200


@workout_bp.get('/workouts/<int:id>')
def get_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return {'error': 'Workout not found'}, 404
    return schema.dump(workout), 200


@workout_bp.post('/workouts')
def create_workout():
    try:
        data = schema.load(request.get_json(silent=True) or {})
        workout = Workout(**data)
        db.session.add(workout)
    except ValidationError as err:
        return {'errors': err.messages}, 422
    except (TypeError, ValueError) as err:
        db.session.rollback()
        return {'error': str(err)}, 422

    error = save_or_rollback()
    if error:
        return error
    return schema.dump(workout), 201


@workout_bp.route('/workouts/<int:id>', methods=['PUT', 'PATCH'])
def update_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return {'error': 'Workout not found'}, 404
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return {'error': 'Request body must be a JSON object.'}, 400
    try:
        data = schema.load(payload, partial=request.method == 'PATCH')
        for key, value in data.items():
            setattr(workout, key, value)
    except ValidationError as err:
        return {'errors': err.messages}, 422
    except (TypeError, ValueError) as err:
        db.session.rollback()
        return {'error': str(err)}, 422
    error = save_or_rollback()
    if error:
        return error
    return schema.dump(workout), 200


@workout_bp.delete('/workouts/<int:id>')
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return {'error': 'Workout not found'}, 404
    db.session.delete(workout)
    error = save_or_rollback()
    if error:
        return error
    return '', 204
