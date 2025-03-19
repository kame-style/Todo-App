from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from auth import get_current_active_user
from database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    """
    Get current user's information
    """
    return current_user


@router.get("/me/todos", response_model=list[schemas.Todo])
def read_user_todos(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all todos for the current user
    """
    return crud.get_user_todos(db, user_id=current_user.id) 