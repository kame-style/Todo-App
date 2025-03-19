# Import required modules
import os  # For accessing environment variables
from sqlalchemy import create_engine  # Core SQLAlchemy function to create a database engine
from sqlalchemy.ext.declarative import declarative_base  # Base class for declarative models
from sqlalchemy.orm import sessionmaker  # Factory for creating database sessions
from dotenv import load_dotenv  # For loading environment variables from .env file

# Load environment variables from .env file
# This allows configuration without hardcoding credentials
load_dotenv()

# Get database connection string from environment variables or use default
# The DATABASE_URL format is: dialect+driver://username:password@host:port/database
# Example: postgresql://postgres:postgres@localhost:5432/todo_db
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/todo_db")

# Create SQLAlchemy engine
# The engine is the central source of connections to the database
# It maintains a pool of connections and provides the interface for acquiring new connections
engine = create_engine(DATABASE_URL)

# Create a sessionmaker class
# This will be used to create new database sessions
# autocommit=False: Changes won't be committed automatically - explicit commits are required
# autoflush=False: Changes won't be flushed to the database before each query
# bind=engine: Connect the session to our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class
# This is used as the base class for all SQLAlchemy models
# Models that inherit from this class will be mapped to database tables
Base = declarative_base()

# Define a dependency function for FastAPI
def get_db():
    """
    FastAPI dependency that provides a database session.
    
    This function creates a new database session for each request and
    ensures it is closed when the request is complete, even if an exception occurs.
    
    The yield statement makes this a generator dependency, which allows
    the database session to be used in the endpoint and then properly closed.
    
    Yields:
        SQLAlchemy Session: A database session for use in API endpoints
        
    Example:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(models.Item).all()
    """
    # Create a new session instance from our SessionLocal factory
    db = SessionLocal()
    try:
        # Yield the session to the endpoint
        yield db
    finally:
        # Ensure the session is closed even if an exception occurs
        # This prevents connection leaks and returns connections to the pool
        db.close() 