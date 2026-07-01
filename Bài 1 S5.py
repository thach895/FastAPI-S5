from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app= FastAPI()

products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]

class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int

@app.post("/products")
def create_product(product:ProductCreate):
    for p in products:
        if p.get("id")== product.code:
            raise HTTPException(
                status_code=400,
                detail="Mã đã tồn tại"
            )
    new_product={
        "id":len(product)+1,
        "code":product.code,
        "name":product.name,
        "price":product.price,
        "stock":product.stock
    }
    
    products.append(new_product)
    return{
        "status_code":201,
        "message":"Tạo thành công"
    }