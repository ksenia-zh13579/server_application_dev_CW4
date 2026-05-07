from pydantic import BaseModel, Field
from fastapi import HTTPException

#task 10.1
class ProductBase(BaseModel):
    title: str
    price: float = Field(gt=0)
    count: int = Field(ge=0)
    description: str

class ProductResponse(ProductBase):
    id: int = Field(ge=0)

class ProductPost(ProductBase):
    pass

class ExceptionNotFoundProductModel(BaseModel):
    status_code: int
    detail: str
    product_id: int 

class ExceptionPostProductModel(BaseModel):
    status_code: int
    detail: str
    product: ProductPost 

class ExceptionNotFoundProduct(HTTPException):
    def __init__(self, status_code: int, detail: str, product_id: int):
        super().__init__(status_code=status_code, detail=detail)
        self.product_id = product_id

class ExceptionPostProduct(HTTPException):
    def __init__(self, status_code: int, detail: str, product: ProductPost):
        super().__init__(status_code=status_code, detail=detail)
        self.product = product

