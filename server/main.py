from fastapi import FastAPI, Depends, HTTPException, status
from models.product import Product
from db.database import session, engine
import DB_Models.Product as ProductModel
from models.CreateProduct import CreateProduct
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


app = FastAPI()

ProductModel.Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def getHome():
    return {"message": "Welcome to the FastAPI server!"}

@app.get("/products")   
def getProducts(db: Session = Depends(get_db)):
    db_products = db.query(ProductModel.Product).all()
    return {"products": db_products}

@app.get("/products/search", response_model=list[Product])
def searchProducts(
    searchText: str,
    db: Session = Depends(get_db)
):
    results = (
        db.query(ProductModel.Product)
        .filter(
            or_(
                ProductModel.Product.product_name.ilike(f"%{searchText}%"),
                ProductModel.Product.description.ilike(f"%{searchText}%")
            )
        )
        .all()
    )

    return results

@app.get("/products/{productId: int}")
def getProductById(productId: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel.Product).filter(ProductModel.Product.product_id == productId).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def addProduct(
    product: CreateProduct,
    db: Session = Depends(get_db)
):
    db_product = ProductModel.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{productId}")
def deleteProduct(productId: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel.Product).filter(ProductModel.Product.product_id == productId).first()
    if not db_product:
        return {"error": "Product not found"}
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"} 

@app.put("/products/{productId}", response_model=Product)
def updateProduct(
    productId: int,
    updatedProduct: CreateProduct,
    db: Session = Depends(get_db)
):
    db_product = (
        db.query(ProductModel.Product)
        .filter(ProductModel.Product.product_id == productId)
        .first()
    )

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = updatedProduct.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_product, field, value)

    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update product")