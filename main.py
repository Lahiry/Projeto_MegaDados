from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
  
f = open('products.json')
products = json.load(f)

class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

app = FastAPI()

# get todos
# get individual
# create individual
# update individual
# delete individual
# error handling

@app.get("/products")
async def get_products():
    return products["products"]

@app.get("/products/{id_product}")
async def get_product(id_product: int):
    for product in products["products"]:
        if product["id"] == id_product:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products")
async def create_product(product: Product):
    if product.id < 0:
        raise HTTPException(status_code=400, detail="Id cannot be negative")

    if product.quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")

    if product.price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative")

    if product.id in [product["id"] for product in products["products"]] or product.name in [product["name"] for product in products["products"]]:
        raise HTTPException(status_code=400, detail="Product already exists")

    if product.name == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    products["products"].append(product.dict())

    with open('products.json', 'w') as f:
        json.dump(products, f)

    return "Product created successfully"

