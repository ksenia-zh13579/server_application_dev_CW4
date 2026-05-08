import pytest
from httpx import AsyncClient
from app.models import ProductResponse, ProductPost, ExceptionNotFoundProductModel, ExceptionPostProductModel

# task 11.2
@pytest.mark.anyio
async def test_get_product_async(async_client: AsyncClient, reset_fake_db, existing_product):
    product_id = existing_product["id"]
    response = await async_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert existing_product == response.json()

@pytest.mark.anyio
async def test_get_nonexisting_async(async_client: AsyncClient, reset_fake_db):
    fake_id = 9999
    response = await async_client.get(f"/products/{fake_id}")
    assert response.status_code == 404
    assert response.json() == ExceptionNotFoundProductModel(
        status_code=404, 
        detail='Product Not Found', 
        product_id=fake_id
    ).model_dump()

@pytest.mark.anyio
async def test_post_product_async(async_client: AsyncClient, reset_fake_db, fake_post_product):
    response = await async_client.post("/products/", json=fake_post_product)
    assert response.status_code == 201
    res_data = response.json()
    assert "id" in res_data
    del res_data["id"]
    assert res_data == fake_post_product

@pytest.mark.anyio
async def test_post_conflict_async(async_client: AsyncClient, reset_fake_db, existing_product):
    exist_copy = existing_product.copy()
    del exist_copy["id"]
    response = await async_client.post("/products/", json=exist_copy)
    assert response.status_code == 409
    assert response.json() == ExceptionPostProductModel(
                status_code=409, 
                detail="Product with this title already exists", 
                product=ProductPost(**exist_copy)
            ).model_dump()

@pytest.mark.anyio
async def test_post_invalid_async(async_client: AsyncClient, reset_fake_db, fake_post_product_invalid):
    response = await async_client.post("/products/", json=fake_post_product_invalid)
    assert response.status_code == 422

@pytest.mark.anyio
async def test_delete_product_async(async_client: AsyncClient, reset_fake_db, existing_product):
    product_id = existing_product["id"]
    delete_response = await async_client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 204
    get_response = await async_client.get(f"/products/{product_id}")
    assert get_response.status_code == 404