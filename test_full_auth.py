from sqlalchemy.orm import sessionmaker
from database import engine
import models
import auth

def test_full_flow():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    email = "newtest@example.com"
    password = "testpassword123"
    full_name = "New Test User"
    
    # 1. Signup
    print(f"--- Testing Signup for {email} ---")
    existing_user = session.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        print("User already exists, deleting for clean test...")
        session.delete(existing_user)
        session.commit()
    
    hashed_password = auth.get_password_hash(password)
    new_user = models.User(email=email, hashed_password=hashed_password, full_name=full_name)
    session.add(new_user)
    session.commit()
    print("Signup successful.")
    
    # 2. Login
    print(f"--- Testing Login for {email} ---")
    user = session.query(models.User).filter(models.User.email == email).first()
    if not user:
        print("Login FAILED: User not found after signup.")
        return
    
    is_valid = auth.verify_password(password, user.hashed_password)
    if is_valid:
        print("Login SUCCESSFUL: Password verified.")
    else:
        print("Login FAILED: Password verification failed.")
        
    session.close()

if __name__ == "__main__":
    test_full_flow()
