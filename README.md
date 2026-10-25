# Workout API

A Flask SQLAlchemy REST API for managing workouts, exercises, and the relationship between them.

## Features

- Manage workouts
- Manage exercises
- Link exercises to workouts with reps, sets, and duration
- Validation and database constraints for safe data entry
- SQLite database support for local development

## Tech Stack

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite

## Project Structure

- `app.py` – application factory and startup entry point
- `seed.py` – populates the database with starter data
- `server/models/` – SQLAlchemy models
- `server/routes/` – Flask route blueprints
- `server/schemas/` – Marshmallow serializers and validation
- `tests/` – smoke tests for the API

## Installation

1. Clone the repository.
2. Open a terminal in the project root.
3. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install Flask Flask-SQLAlchemy Flask-Migrate Marshmallow SQLAlchemy pytest
```

5. Or use the included Pipfile with pipenv:

```bash
pip install pipenv
pipenv install --dev
pipenv shell
```

## Run the App

```bash
python app.py
```

The app runs on:

- http://127.0.0.1:5555/

## Available Endpoints

- `GET /`
- `GET /workouts`
- `GET /workouts/<id>`
- `POST /workouts`
- `PUT /workouts/<id>`
- `PATCH /workouts/<id>`
- `DELETE /workouts/<id>`
- `GET /exercises`
- `GET /exercises/<id>`
- `POST /exercises`
- `PUT /exercises/<id>`
- `PATCH /exercises/<id>`
- `DELETE /exercises/<id>`
- `GET /workout_exercises`
- `GET /workout_exercises/<id>`
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`
- `PUT /workout_exercises/<id>`
- `PATCH /workout_exercises/<id>`
- `DELETE /workout_exercises/<id>`

## Seed the Database

```bash
python seed.py
```

This creates sample workout and exercise data so the API has starter records to work with.

## Testing

```bash
pytest -q
```

## Notes

The app uses SQLite by default, so no external database setup is required for local development.
