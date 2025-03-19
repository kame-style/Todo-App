from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from auth import get_current_active_user
from database import get_db

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=List[schemas.Todo])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get all todos for the current user
    """
    return crud.get_user_todos(db, user_id=current_user.id)


@router.post("/", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Create a new todo for the current user
    """
    return crud.create_todo(db=db, todo=todo, user_id=current_user.id)


@router.get("/{todo_id}", response_model=schemas.Todo)
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get a specific todo by ID that belongs to the current user
    """
    # Get the todo that belongs to the current user
    db_todo = crud.get_user_todo(db, user_id=current_user.id, todo_id=todo_id)
    
    # Check if todo exists and belongs to user
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return db_todo


@router.put("/{todo_id}", response_model=schemas.Todo)
def update_todo(
    todo_id: int,
    todo: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Update a todo that belongs to the current user
    """
    # Update the todo that belongs to the current user
    db_todo = crud.update_todo(db, todo_id=todo_id, todo=todo, user_id=current_user.id)
    
    # Check if todo exists and belongs to user
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return db_todo


@router.delete("/{todo_id}", response_model=schemas.Todo)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Delete a todo that belongs to the current user
    """
    # Delete the todo that belongs to the current user
    db_todo = crud.delete_todo(db, todo_id=todo_id, user_id=current_user.id)
    
    # Check if todo exists and belongs to user
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return db_todo 