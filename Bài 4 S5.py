from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]


class ProductUpdate(BaseModel):
    code: str
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    # Kiểm tra sản phẩm có tồn tại hay không
    current_product = None
    for item in products:
        if item["id"] == product_id:
            current_product = item
            break

    if current_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Kiểm tra mã sản phẩm có bị trùng hay không
    for item in products:
        if item["code"] == product.code and item["id"] != product_id:
            raise HTTPException(
                status_code=400,
                detail="Product code already exists"
            )

    # Cập nhật thông tin sản phẩm
    current_product["code"] = product.code
    current_product["name"] = product.name
    current_product["price"] = product.price
    current_product["stock"] = product.stock

    return {
        "message": "Product updated successfully",
        "data": current_product
    }