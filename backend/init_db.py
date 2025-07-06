from database import Base, engine, Session
from models import User, Order

Base.metadata.create_all(bind=engine)