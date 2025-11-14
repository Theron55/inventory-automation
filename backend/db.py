from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Using SQLite for now (simple local file-based database)
DATABASE_URL = "sqlite:///inventory.db"

# Create the SQLAlchemy engine (handles the connection to the database)
engine = create_engine(
    DATABASE_URL,
    echo=True, # Prints SQL queries to the console — helpful while learning
)

# SessionLocal will be used in routes to talk to the database
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Base class that our models will inherit from
Base = declarative_base()

