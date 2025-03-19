# Import necessary modules
from sqlalchemy.orm import Session  # For typing the database session
import models  # SQLAlchemy models
import schemas  # Pydantic schemas
from auth import get_password_hash  # Password hashing utility

# User operations
def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user"""
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Create a new user with the hashed password
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )
    
    # Add to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def get_user_by_email(db: Session, email: str):
    """Get a user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """Get a user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_todos(db: Session, user_id: int):
    """Get all todos for a user"""
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).all()


# Todo operations
def get_todos(db: Session, skip: int = 0, limit: int = 100):
    """Get all todos with pagination"""
    return db.query(models.Todo).offset(skip).limit(limit).all()


def get_user_todo(db: Session, user_id: int, todo_id: int):
    """Get a specific todo for a user"""
    return db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.owner_id == user_id
    ).first()


def get_todo(db: Session, todo_id: int):
    """Get a todo by ID"""
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    """Create a new todo for a user"""
    # Create a Todo model instance from the schema
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    
    # Add the new todo to the session
    db.add(db_todo)
    
    # Commit the transaction to the database
    db.commit()
    
    # Refresh the instance to load any database-generated values (like ID)
    db.refresh(db_todo)
    
    # Return the created todo
    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate, user_id: int):
    """Update a user's todo"""
    # Find the todo to update that belongs to the user
    db_todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.owner_id == user_id
    ).first()
    
    if db_todo:
        # Get data from the schema, excluding unset fields
        update_data = todo.dict(exclude_unset=True)
        
        # Update each field on the model
        for key, value in update_data.items():
            setattr(db_todo, key, value)
            
        # Commit the changes to the database
        db.commit()
        
        # Refresh the instance to load any updated values
        db.refresh(db_todo)
    
    # Return the updated todo (or None if not found)
    return db_todo


def delete_todo(db: Session, todo_id: int, user_id: int):
    """Delete a user's todo"""
    # Find the todo to delete that belongs to the user
    db_todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.owner_id == user_id
    ).first()
    
    if db_todo:
        # Remove the todo from the database
        db.delete(db_todo)
        
        # Commit the transaction
        db.commit()
    
    # Return the deleted todo (or None if not found)
    return db_todo 