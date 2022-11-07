from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class MovementBase(BaseModel):
    product_id: int
    quantity: int

class MovementCreate(MovementBase):
    pass

class Movement(MovementBase):
    id: int

    class Config:
        orm_mode = True

