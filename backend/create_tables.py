from database import engine, Base
from models import Customer, Account, Transaction, AMLRule, Alert

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")