from database import engine
import models

def test_connection():
    try:
        # Try to create tables
        models.Base.metadata.create_all(bind=engine)
        print("Connection successful and tables created!")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection() 