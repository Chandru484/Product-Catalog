from sqlalchemy.orm import sessionmaker
from database import engine
import models
import auth

def test_login(email, password):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(models.User).filter(models.User.email == email).first()
    if not user:
        print(f"User {email} not found.")
    else:
        is_valid = auth.verify_password(password, user.hashed_password)
        print(f"User found: {user.email}")
        print(f"Password '{password}' valid: {is_valid}")
    session.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        test_login(sys.argv[1], sys.argv[2])
    else:
        # Try with the user I found earlier
        # I don't know the password, but I can try hashing one and then verifying it
        test_login("chandru4842193@gmail.com", "password") # Probably wrong
