from faker import Faker
from fastapi.testclient import TestClient
from main import app
import pytest


fake = Faker()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def video_data():
    return {
        "id": fake.uuid4(),
        "url": fake.url(),
        "title": fake.sentence(),
        "tags": [fake.word(), fake.word(), fake.word()],
        "views": fake.random_int(),
        "unique_views": fake.random_int(),
    }
    