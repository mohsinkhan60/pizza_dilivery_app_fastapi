from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# creates the connection between your app and PostgreSQL database
engine=create_engine('postgresql://postgres:Mohsin123khan@localhost/pizza_delivery',
    echo=True
)

# creates the base class for your tables (models)
Base=declarative_base()

# Talk to the database (insert, read, delete, etc.)
Session=sessionmaker(bind=engine)