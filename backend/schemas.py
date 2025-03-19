# Import necessary modules for data validation and typing
from pydantic import BaseModel, EmailStr  # Base class for data validation and email validation
from datetime import datetime  # For timestamp fields
from typing import Optional, List  # For marking fields as optional and typing lists

# several Pydantic models for data validation and serialization #Are not directly tied to the database


# User schemas
class UserBase(BaseModel):
    """Base Pydantic model for User items."""
    email: EmailStr


class UserCreate(UserBase):
    """Schema used when creating a new user."""
    password: str


class User(UserBase):
    """Schema used for User responses."""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserInDB(User):
    """Schema that includes hashed password - for internal use only."""
    hashed_password: str


# Token schemas
class Token(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload."""
    email: Optional[str] = None


# Todo schemas
class TodoBase(BaseModel):
    """
    Base Pydantic model for Todo items.
    Contains common fields shared by multiple schemas.
    
    This class serves as a parent class for other Todo-related schemas,
    establishing the common fields and their validation rules.
    """
    title: str  # Required field - the title of the todo item
    description: Optional[str] = None  # Optional description with None default
    completed: Optional[bool] = False  # Whether the todo is completed, defaults to False


class TodoCreate(TodoBase):
    """
    Schema used when creating a new Todo.
    
    Inherits all fields from TodoBase without adding new ones.
    This class is used to validate the request body when creating a new todo.
    
    Note: id, created_at, and updated_at are not included as they're generated 
    by the database, not provided by the client.
    """
    pass  # No additional fields required for creation


class TodoUpdate(BaseModel):
    """
    Schema used when updating an existing Todo.
    
    All fields are optional since updates might modify only a subset of fields.
    This allows partial updates (PATCH-like behavior) through PUT requests.
    """
    title: Optional[str] = None  # Optional title update
    description: Optional[str] = None  # Optional description update
    completed: Optional[bool] = None  # Optional completed status update


class Todo(TodoBase):
    """
    Schema used for Todo responses.
    
    Contains all fields from TodoBase plus the database-generated fields.
    This represents the complete Todo item as returned by the API.
    """
    id: int  # Database-generated primary key
    owner_id: int  # ID of the user who owns this todo
    created_at: datetime  # Timestamp when the todo was created
    updated_at: Optional[datetime] = None  # Timestamp when the todo was last updated

    class Config:
        """
        Pydantic configuration options for the Todo model.
        """
        orm_mode = True  # Enables ORM mode which allows Pydantic to read data from ORM objects
        # ORM mode allows the schema to work with SQLAlchemy models directly
        # Without this, Pydantic would only work with dictionaries


class UserWithTodos(User):
    """User schema that includes the user's todos."""
    todos: List[Todo] = [] 