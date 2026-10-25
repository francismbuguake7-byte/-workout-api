import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


def test_health_check():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['message'] == 'Workout API is running'


def test_exercises_endpoint_returns_list():
    client = app.test_client()
    response = client.get('/exercises')
    assert response.status_code == 200
    assert isinstance(response.json, list)
