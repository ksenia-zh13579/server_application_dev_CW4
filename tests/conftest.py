from fastapi.testclient import TestClient
import pytest
from faker import Faker
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.models import ProductResponse, ProductPost
from app.db.fake_db import products

# task 11.1
@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def reset_fake_db():
    products.clear()
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
    # return products

# task 11.2
fake = Faker()

@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_cl:
        yield async_cl

@pytest.fixture
def fake_post_product():
    return ProductPost(
        title=fake.unique.sentence(nb_words=4),
        price=round(fake.pyfloat(min_value=0.01, max_value=9999.99), 2),
        count=fake.random_int(min=0, max=1000),
        description=fake.paragraph(nb_sentences=3),
    ).model_dump()

@pytest.fixture
def fake_post_product_invalid(fake_post_product):
    product = fake_post_product.copy()
    product["price"] = -15.0
    return product

@pytest.fixture
async def existing_product(async_client, fake_post_product):
    response = await async_client.post("/products/", json=fake_post_product)
    assert response.status_code == 201
    return response.json()