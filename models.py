from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    qty = Column(Integer, default=1)
    rate = Column(Float)
    image_url = Column(String)  # Front View
    back_image_url = Column(String, nullable=True)  # Back View
    weight = Column(Float, nullable=True)
    rc_rate_kg_invoice = Column(Float, nullable=True)
    machining_cost_invoice = Column(Float, nullable=True)
    rate_piece_invoice = Column(Float, nullable=True)
    rc_rate_kg_no_invoice = Column(Float, nullable=True)
    machining_cost_no_invoice = Column(Float, nullable=True)
    rate_piece_no_invoice = Column(Float, nullable=True)
    selling_price_invoice = Column(Float, nullable=True)
    selling_price_no_invoice = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
