from database import Base, engine
from models import User, Todo  # Import models to ensure they are registered

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)
print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Database reset complete!") 