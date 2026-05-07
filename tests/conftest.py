from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.models import ProductResponse
from app.db.fake_db import products

# task 11.1
@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def reset_fake_db():
    products[:] = [
        ProductResponse(
            id=1, 
            title='notebook', 
            price=512, 
            count=100, 
            description='notelook with lines, 100 pages'
        ),
        ProductResponse(
            id=2, 
            title='pen', 
            price=120, 
            count=120, 
            description='roller pen, blue'
        ),
    ]
    return products