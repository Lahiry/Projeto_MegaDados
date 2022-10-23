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

description = """
BackendAyres API te ajuda a gerenciar melhor seu estoque. 🚀

## Itens

Você poderá:

* **Criar itens**.
* **Atualizar itens**.
* **Deletar itens**.
* **Puxar itens**.
"""

app = FastAPI(
    title="BackendAyres",
    description=description,
    version="0.0.1",
    contact={
        "name": "Raphael Lahiry e Rodrigo Coelho",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

tags_metadata = [
    {
        "name": "Get products",
        "description": "Listagem de todos os produtos em estoque",
    },
    {
        "name": "Get product",
        "description": "Lista produto específico do estoque",
    },
    {
        "name": "Create product",
        "description": "Cria um produto no estoque",
    },
    {
        "name": "Delete product",
        "description": "Deleta um produto do estoque",
    },
    {
        "name": "Update product",
        "description": "Atualiza um produto no estoque",
    },
]

# Auxiliar functions

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


# Routes

@app.get("/products", tags=["Get products"], summary="Listagem de todos os produtos em estoque")
async def get_products():
    return products

@app.get("/product/{id_product}", tags=["Get product"], summary="Lista produto específico do estoque")
async def get_product(id_product: int):
    for product in products:
        if product["id"] == id_product:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/product", tags=["Create product"], summary="Cria um produto no estoque")
async def create_product(product: Product):

    verify_restrictions(product)
    save_product(product)

    return "Product created successfully"

@app.patch("/product", tags=["Update product"], summary="Atualiza um produto no estoque")
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

@app.delete("/product/{id_product}", tags=["Delete product"], summary="Deleta um produto do estoque")
async def delete_product(id_product: int):

    if id_product < 0:
        raise HTTPException(status_code=400, detail="Id cannot be negative")

    if id_product not in [product["id"] for product in products["products"]]:
        raise HTTPException(status_code=400, detail="Product doens't exists")

    filtered_products = [product for product in products if product['id'] != id_product]

    with open('products.json', 'w') as f:
        json.dump(filtered_products, f)
    
    return "Product deleted successfully"