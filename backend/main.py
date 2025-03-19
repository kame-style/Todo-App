# Import necessary modules
from fastapi import FastAPI, Depends, HTTPException, status  # FastAPI framework components
from fastapi.middleware.cors import CORSMiddleware  # For handling Cross-Origin Resource Sharing
from sqlalchemy.orm import Session  # For database session typing
from typing import List  # For type annotations

# Import local modules
import crud  # Contains CRUD operations for the database
import models  # Contains SQLAlchemy models
import schemas  # Contains Pydantic schemas for request/response validation
from database import engine, get_db  # Database connection and session dependency

# Create tables in the database based on SQLAlchemy models
# This will create tables if they don't exist already
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI(title="Todo API")

# Add CORS middleware to allow cross-origin requests
# This is necessary for the frontend to communicate with the API from a different domain/port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,  # Allows cookies to be included in requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Root endpoint - simple health check
@app.get("/")
def read_root():
    """Return a welcome message to confirm the API is running."""
    return {"message": "Welcome to the Todo API"}


# GET endpoint to retrieve all todos
@app.get("/todos/", response_model=List[schemas.Todo])
def read_todos(db: Session = Depends(get_db)):
    """
    Retrieve all todos from the database.
    
    Args:
        db: Database session (injected by FastAPI dependency)
    
    Returns:
        List of all Todo objects
    """
    todos = crud.get_todos(db)
    return todos


# GET endpoint to retrieve a specific todo by ID
@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single todo by ID.
    
    Args:
        todo_id: ID of the todo to retrieve
        db: Database session
        
    Returns:
        Todo object if found
        
    Raises:
        HTTPException: 404 if todo not found
    """
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


# POST endpoint to create a new todo
@app.post("/todos/", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new todo.
    
    Args:
        todo: TodoCreate object containing todo data
        db: Database session
        
    Returns:
        Created Todo object
        
    Note:
        Uses HTTP 201 status code to indicate resource creation
    """
    return crud.create_todo(db=db, todo=todo)


# PUT endpoint to update an existing todo
@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    """
    Update an existing todo.
    
    Args:
        todo_id: ID of the todo to update
        todo: TodoUpdate object with fields to update
        db: Database session
        
    Returns:
        Updated Todo object
        
    Raises:
        HTTPException: 404 if todo not found
    """
    db_todo = crud.update_todo(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


# DELETE endpoint to remove a todo
@app.delete("/todos/{todo_id}", response_model=schemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Delete a todo.
    
    Args:
        todo_id: ID of the todo to delete
        db: Database session
        
    Returns:
        Deleted Todo object
        
    Raises:
        HTTPException: 404 if todo not found
    """
    db_todo = crud.delete_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo 