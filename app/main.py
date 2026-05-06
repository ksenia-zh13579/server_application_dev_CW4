from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from app.db.fake_db import products, get_product
from app.models import ProductResponse, ProductPost, ExceptionGetProduct, ExceptionPostProduct, ExceptionGetProductModel, ExceptionPostProductModel

app = FastAPI()

#task 10.1
@app.exception_handler(ExceptionGetProduct)
async def exception_get_prod_handler(request: Request, exc: ExceptionGetProduct) -> JSONResponse:
    error = jsonable_encoder(ExceptionGetProductModel(status_code=exc.status_code, detail=exc.detail, product_id=exc.product_id))
    return JSONResponse(status_code=exc.status_code, content=error)

@app.exception_handler(ExceptionPostProduct)
async def exception_post_prod_handler(request: Request, exc: ExceptionPostProduct) -> JSONResponse:
    error = jsonable_encoder(ExceptionPostProductModel(status_code=exc.status_code, detail=exc.detail, product=exc.product))
    return JSONResponse(status_code=exc.status_code, content=error)

#task 10.2
@app.exception_handler(RequestValidationError)
async def exception_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    )

@app.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Product by ID.",
    description="The endpoint returns product by ID.",
    responses={
        status.HTTP_200_OK: {'model': ProductResponse},
        status.HTTP_404_NOT_FOUND: {'model': ExceptionGetProductModel},
    },
)
async def read_item(product_id: int):
    product = get_product(product_id)
    if product is None:
        raise ExceptionGetProduct(status_code=404, detail='Product Not Found', product_id=product_id)
    return product

@app.post(
    "/products/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create New Product.",
    description="The endpoint creates new product in the database.",
    responses={
        status.HTTP_201_CREATED: {'model': ProductResponse},
        status.HTTP_409_CONFLICT: {'model': ExceptionPostProductModel},
    },
)
async def create_item(product: ProductPost):
    for existing_pr in products:
        if existing_pr.title == product.title:
            raise ExceptionPostProduct(status_code=409, detail="Product with this title already exists", product=product)
    product_in_db = ProductResponse(
        id=products[-1].id + 1,
        title=product.title,
        price=product.price,
        count=product.count,
        description=product.description
    )
    products.append(product_in_db)
    return product_in_db