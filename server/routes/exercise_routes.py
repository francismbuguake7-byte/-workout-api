from flask import Blueprint, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from server.models import Exercise, db
from server.schemas import ExerciseSchema

exercise_bp = Blueprint('exercises', __name__)
schema = ExerciseSchema()
many_schema = ExerciseSchema(many=True)


def save_or_rollback():
    try:
        db.session.commit()
        return None
    except IntegrityError:
        db.session.rollback()
        return {'error': 'An exercise with that name may already exist.'}, 409
    except SQLAlchemyError:
        db.session.rollback()
        return {'error': 'Database operation failed.'}, 500


@exercise_bp.get('/exercises')
def list_exercises():
    return many_schema.dump(Exercise.query.order_by(Exercise.id).all()), 200


@exercise_bp.get('/exercises/<int:id>')
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return {'error': 'Exercise not found'}, 404
    return schema.dump(exercise), 200


@exercise_bp.post('/exercises')
def create_exercise():
    try:
        data = schema.load(request.get_json(silent=True) or {})
        exercise = Exercise(**data)
        db.session.add(exercise)
    except ValidationError as err:
        return {'errors': err.messages}, 422
    except (TypeError, ValueError) as err:
        db.session.rollback()
        return {'error': str(err)}, 422
    error = save_or_rollback()
    if error:
        return error
    return schema.dump(exercise), 201


@exercise_bp.route('/exercises/<int:id>', methods=['PUT', 'PATCH'])
def update_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return {'error': 'Exercise not found'}, 404
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return {'error': 'Request body must be a JSON object.'}, 400
    try:
        data = schema.load(payload, partial=request.method == 'PATCH')
        for key, value in data.items():
            setattr(exercise, key, value)
    except ValidationError as err:
        return {'errors': err.messages}, 422
    except (TypeError, ValueError) as err:
        db.session.rollback()
        return {'error': str(err)}, 422
    error = save_or_rollback()
    if error:
        return error
    return schema.dump(exercise), 200


@exercise_bp.delete('/exercises/<int:id>')
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return {'error': 'Exercise not found'}, 404
    db.session.delete(exercise)
    error = save_or_rollback()
    if error:
        return error
    return '', 204
