# Import necessary modules
from sqlalchemy.orm import Session  # For typing the database session
import models  # SQLAlchemy models
import schemas  # Pydantic schemas


def get_todos(db: Session):
    return db.query(models.Todo).all()


def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def create_todo(db: Session, todo: schemas.TodoCreate):
    # Create a Todo model instance from the schema
    # ** unpacks the dictionary returned by todo.dict() into keyword arguments
    db_todo = models.Todo(**todo.dict())
    
    # Add the new todo to the session
    db.add(db_todo)
    
    # Commit the transaction to the database
    db.commit()
    
    # Refresh the instance to load any database-generated values (like ID)
    db.refresh(db_todo)
    
    # Return the created todo
    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    # Find the todo to update
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    
    if db_todo:
        # Get data from the schema, excluding unset fields
        # exclude_unset=True means only fields that were explicitly set will be included
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


def delete_todo(db: Session, todo_id: int):
    # Find the todo to delete
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    
    if db_todo:
        # Remove the todo from the database
        db.delete(db_todo)
        
        # Commit the transaction
        db.commit()
    
    # Return the deleted todo (or None if not found)
    return db_todo 