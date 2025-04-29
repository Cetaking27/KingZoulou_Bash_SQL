from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
import json

# from fastapi.middleware.cors import CORSMiddleware
# from routers import users, items, auth  # Importing routers from the routers package

# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
import os

app = FastAPI()


# adding data to the app
with open('products.json', 'r', encoding="utf-*") as f:
    products = json.load(f)
    
cart = []

# model for product to add to cart
class Product(BaseModel):
    Product_id: int
    name : str
    price: float
    quantity: int 
    description: str

#model for the desription of the product
@app.get("/products", response_model=List[Product])
def get_products_list():
    return [
        Product(
            Product_id=product["Product_id"],
            name=product["name"],
            price=product["price"],
            quantity=product["quantity"],
            description=product["description"]
        )
        for product in products
    ]

#model for getting detail of the product 
@app.get("/products/{product_id}", response_model=Product)
def get_product_detail(product_id: int):
    for product in products:
        if product["Product_id"] == product_id:
            return Product(
                Product_id=product["Product_id"],
                name=product["name"],
                price=product["price"],
                quantity=product["quantity"],
                description=product["description"]
            )
    raise HTTPException(status_code=404, detail="Товар не найден")




#model for puting the product in the cart
@app.post("/cart", response_model=Product)
def add_to_cart(product: Product):
    for item in products:
        if item["Product_id"] == product.Product_id:
            cart.append(item)
            return Product(
                Product_id=item["Product_id"],
                name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                description=item["description"]
            )
    raise HTTPException(status_code=404, detail="Товар не найден")


#model for viewing the cart
@app.get("/cart")
def view_cart():
    return [
        Product(
            Product_id=product["Product_id"],
            name=product["name"],
            price=product["price"],
            quantity=product["quantity"],
            description=product["description"]
        )
        for product in cart
    ]