from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def verify_restrictions(product: Product, verify_product_exists: bool = True):
#     if product.id < 0:
#         raise HTTPException(status_code=400, detail="Id cannot be negative")

#     if product.quantity < 0:
#         raise HTTPException(status_code=400, detail="Quantity cannot be negative")

#     if product.price < 0:
#         raise HTTPException(status_code=400, detail="Price cannot be negative")

#     if verify_product_exists:
#         if product.id in [product["id"] for product in products] or product.name in [product["name"] for product in products]:
#             raise HTTPException(status_code=400, detail="Product already exists")

#     if product.name == "":
#         raise HTTPException(status_code=400, detail="Name cannot be empty")

# def save_product(product: Product):
#     products.append(product.dict())
#     with open('products.json', 'w') as f:
#         json.dump(products, f)


# Routes

# PRODUCTS

@app.get("/products", response_model=list[schemas.Product], tags=["Get products"], summary="Listagem de todos os produtos em estoque")
async def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.get("/product/{id_product}", response_model=schemas.Product, tags=["Get product"], summary="Lista produto específico do estoque")
async def get_product(id_product: int, db: Session = Depends(get_db)):
    return crud.get_product(db, id_product)

@app.post("/product", response_model=schemas.Product, tags=["Create product"], summary="Cria um produto no estoque")
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.patch("/product", response_model=schemas.Product, tags=["Update product"], summary="Atualiza um nome e/ou preço de um produto no estoque")
async def update_product(product: schemas.Product, db: Session = Depends(get_db)):
    return crud.patch_product(db, product, product.id)

@app.delete("/product/{id_product}", response_model=schemas.Product, tags=["Delete product"], summary="Deleta um produto do estoque")
async def delete_product(id_product: int, db: Session = Depends(get_db)):
    return crud.delete_product(db, id_product)


# MOVEMENTS

@app.get("/movements", response_model=list[schemas.Movement], tags=["Get movements"], summary="Listagem de todas as movimentações")
async def get_moviments(db: Session = Depends(get_db)):
    return crud.get_movements(db)

@app.get("/movements/{movement_id}", response_model=schemas.Movement, tags=["Get movement"], summary="Lista movimentação específica do estoque")
async def get_product(movement_id: int, db: Session = Depends(get_db)):
    return crud.get_movement(db, movement_id)

@app.post("/movement", response_model=schemas.Movement, tags=["Create movement"], summary="Cria uma movimentação do estoque")
async def create_movement(movement: schemas.MovementCreate, db: Session = Depends(get_db)):
    return crud.create_movement(db=db, movement=movement)

@app.delete("/movement/{id_movement}", response_model=schemas.Movement, tags=["Delete movement"], summary="Deleta uma movimentação do estoque")
async def delete_movement(id_movement: int, db: Session = Depends(get_db)):
    return crud.delete_movement(db, id_movement)
