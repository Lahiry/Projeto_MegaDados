from sqlalchemy.orm import Session

import models, schemas

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def patch_product(db: Session, updated_product: schemas.Product, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    db_product.name = updated_product.name
    db_product.price = updated_product.price
    db.commit()
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product

def get_movements(db: Session):
    return db.query(models.Movement).all()

def get_movement(db: Session, movement_id: int):
    return db.query(models.Movement).filter(models.Movement.id == movement_id).first()

def create_movement(db: Session, movement: schemas.MovementCreate):
    db_movement = models.Movement(**movement.dict())
    db.add(db_movement)

    db_product = db.query(models.Product).filter(models.Product.id == movement.product_id).first()
    db_product.quantity += movement.quantity

    db.commit()
    db.refresh(db_movement)

    return db_movement

def delete_movement(db: Session, movement_id: int):
    db_movement = db.query(models.Movement).filter(models.Movement.id == movement_id).first()
    db.delete(db_movement)
    db.commit()
    return db_movement

