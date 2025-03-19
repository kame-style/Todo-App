# Import necessary SQLAlchemy components
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey  # Column types
from sqlalchemy.sql import func  # SQL functions for default values
from sqlalchemy.orm import relationship  # For defining relationships between models
from database import Base  # Base class for declarative models

# User model for authentication
class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    
    This class defines the database schema for storing user accounts.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to todos - one user can have many todos
    todos = relationship("Todo", back_populates="owner")

# SQLAlchemy ORM model that defines the database table structure
class Todo(Base):
    """
    SQLAlchemy model for the 'todos' table.
    
    This class defines the database schema for storing todo items.
    It maps Python attributes to database columns.
    SQLAlchemy handles the ORM (Object-Relational Mapping) between 
    this class and the database table.
    """
    __tablename__ = "todos"  # Name of the database table

    # Primary key - unique identifier for each todo
    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing by default
    
    # Main fields
    title = Column(String, index=True)  # Indexed for faster lookups
    description = Column(String)  # Text description of the todo item
    completed = Column(Boolean, default=False)  # Status flag
    
    # Foreign key to link todo to a user
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship to user - many todos can belong to one user
    owner = relationship("User", back_populates="todos")
    
    # Timestamp fields with automatic values
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Set when record is created
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # Auto-updated when record changes
    
    # Note: server_default=func.now() uses the database server's timestamp function
    # onupdate=func.now() automatically updates the timestamp when the record is updated 