from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
  
f = open('stock.json')
products = json.load(f)['products']

class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

app = FastAPI()

# update individual
# delete individual
# error handling

def verify_restrictions(product: Product, verify_product_exists: bool = True):
    if product.id < 0:
        raise HTTPException(status_code=400, detail="Id cannot be negative")

    if product.quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")

    if product.price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative")

    if verify_product_exists:
        if product.id in [product["id"] for product in products["products"]] or product.name in [product["name"] for product in products["products"]]:
            raise HTTPException(status_code=400, detail="Product already exists")

    if product.name == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")

def save_product(product: Product):
    products.append(product.dict())
    with open('products.json', 'w') as f:
        json.dump(products, f)


@app.get("/products")
async def get_products():
    return products

@app.get("/product/{id_product}")
async def get_product(id_product: int):
    for product in products:
        if product["id"] == id_product:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/product")
async def create_product(product: Product):

    verify_restrictions(product)
    save_product(product)

    return "Product created successfully"

@app.patch("/product")
async def update_product(product: Product):

    verify_restrictions(product, False)

    update_product = product.dict()

    for stock_product in products:
        if stock_product["id"] == update_product["id"]:
            stock_product["name"] = update_product["name"]
            stock_product["price"] = update_product["price"]
            stock_product["quantity"] = update_product["quantity"]
            break

    with open('products.json', 'w') as f:
        json.dump(products, f)

    return "Product updated successfully"

@app.delete("/product/{id_product}")
async def delete_product(id_product: int):

    if id_product < 0:
        raise HTTPException(status_code=400, detail="Id cannot be negative")

    if id_product not in [product["id"] for product in products["products"]]:
        raise HTTPException(status_code=400, detail="Product doens't exists")

    filtered_products = [product for product in products if product['id'] != id_product]

    with open('products.json', 'w') as f:
        json.dump(filtered_products, f)
    
    return "Product deleted successfully"