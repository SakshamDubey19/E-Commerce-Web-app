from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
import sqlite3

db_session = sqlite3.connect('ecommerce.db')





Base = declarative_base()
declarative_base=sessionmaker

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50),nullable=False)
    address = Column(String(50),nullable=False)

class Product(Base):
    __tablename__ = 'product_name'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)

engine = create_engine('sqlite:///ecommerce.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

results = session.query(User).all()
for row in results:
    print(row.id,row.username)
