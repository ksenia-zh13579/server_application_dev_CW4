import pytest
from app.models import ProductResponse, ProductPost, ExceptionNotFoundProductModel, ExceptionPostProductModel
from app.db.fake_db import products

@pytest.mark.parametrize(
    "product_id, exp_status, exp_result",
    [
        (1, 200, ProductResponse(
            id=1, 
            title='notebook', 
            price=512, 
            count=100, 
            description='notelook with lines, 100 pages'
        ).model_dump()),
        (3, 404, ExceptionNotFoundProductModel(
            status_code=404, 
            detail='Product Not Found', 
            product_id=3
        ).model_dump()),
        (3.4, 422, None)
    ]
)
def test_get_product(product_id, exp_status, exp_result, client, reset_fake_db):
    params = {"product_id": product_id}
    response = client.get(f"/products/{product_id}", params=params)
    assert response.status_code == exp_status
    if exp_status != 422:
        assert response.json() == exp_result

@pytest.mark.parametrize(
    "product_id, exp_status, exp_result",
    [
        (1, 204, {}),
        (3, 404, ExceptionNotFoundProductModel(
            status_code=404, 
            detail='Deleting Attempt Failed: Product Not Found', 
            product_id=3
        ).model_dump()),
        (3.4, 422, None)
    ]
)
def test_delete_product(product_id, exp_status, exp_result, client, reset_fake_db):
    params = {"product_id": product_id}
    response = client.delete(f"/products/{product_id}", params=params)
    assert response.status_code == exp_status
    if exp_status == 404:
        assert response.json() == exp_result

@pytest.mark.parametrize(
    "product, exp_status, exp_result",
    [
        (
            ProductPost(
                title='pencil', 
                price=87, 
                count=120, 
                description='graphite pencil, black'
            ).model_dump(), 
            201, 
            ProductResponse(
                id=3, 
                title='pencil', 
                price=87, 
                count=120, 
                description='graphite pencil, black'
            ).model_dump()
        ),
        (
            ProductPost(
                title='notebook', 
                price=512, 
                count=100, 
                description='notelook with lines, 100 pages'
            ).model_dump(), 
            409, 
            ExceptionPostProductModel(
                status_code=409, 
                detail="Product with this title already exists", 
                product=ProductPost(
                    title='notebook', 
                    price=512, 
                    count=100, 
                    description='notelook with lines, 100 pages'
                )
            ).model_dump()
        ),
        ({"title": "scissors"}, 422, None)
    ]
)
def test_post_product(product, exp_status, exp_result, client, reset_fake_db):
    response = client.post("/products/", json=product)
    assert response.status_code == exp_status
    if exp_status != 422:
        assert response.json() == exp_result
