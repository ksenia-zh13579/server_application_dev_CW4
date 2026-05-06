from app.models import ProductResponse

products = [
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

def get_product(id: int) -> ProductResponse:
    for product in products:
        if product.id == id:
            return product
    return None