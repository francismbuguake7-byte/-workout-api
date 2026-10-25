from routes.workout_routes import workout_bp
from routes.exercise_routes import exercise_bp
from routes.workout_exercise_routes import we_bp


def register_routes(app):
   
    app.register_blueprint(workout_bp)
    app.register_blueprint(exercise_bp)
    app.register_blueprint(we_bp)
