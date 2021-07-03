from sqlalchemy import (create_engine, Column, Integer,
                        String, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column('Product Name', String)
    product_quantity = Column('Quantity', Integer)
    product_price = Column('Price', Integer)
    date_updated = Column('Date', Date)

    def __repr__(self):
        return (f'Product Name: {self.product_name} | Quantity: {self.product_quantity} | Price: {self.product_price} | Date: {self.date_updated}')