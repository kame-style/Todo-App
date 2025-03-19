# Import necessary modules
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # For handling Cross-Origin Resource Sharing

# Import local modules
import models  # Contains SQLAlchemy models
from database import engine  # Database connection
from routers import auth, users, todos  # Router modules

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

# Include the routers
app.include_router(auth.router)  # Auth routes (login, register)
app.include_router(users.router)  # User routes
app.include_router(todos.router)  # Todo routes


# Root endpoint - simple health check
@app.get("/")
def read_root():
    """Return a welcome message to confirm the API is running."""
    return {"message": "Welcome to the Todo API"} 