from flask import Flask
from flask_migrate import Migrate

from models import db
from routes import register_routes

migrate = Migrate()


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    register_routes(app)

    @app.get('/')
    def index():
        return {
            'message': 'Workout API is running',
            'endpoints': ['/workouts', '/exercises', '/workout_exercises'],
        }, 200

    @app.errorhandler(404)
    def not_found(_error):
        return {'error': 'Resource not found'}, 404

    return app


app = create_app()


if __name__ == '__main__':
    app.run(port=5555, debug=True)
