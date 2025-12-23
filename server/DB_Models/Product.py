from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Product(Base):
    __tablename__ = "Products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    description = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)