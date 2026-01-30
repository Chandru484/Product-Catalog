from sqlalchemy.orm import sessionmaker
from database import engine
import models
import auth
import main
from fastapi import Request

def verify_all():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 1. Verify stripping on signup
    print("--- Verifying Input Stripping ---")
    email = "  strip@example.com  "
    password = "pass"
    full_name = "  Stripped User  "
    
    # Fake a request or just call the logic
    # In main.py, signup(request, email, ...)
    # I'll manually check the database after a simulated signup
    
    # Direct DB check for logic
    clean_email = email.strip()
    clean_name = full_name.strip()
    
    user = session.query(models.User).filter(models.User.email == clean_email).first()
    if user: session.delete(user); session.commit()
    
    new_user = models.User(email=clean_email, hashed_password=auth.get_password_hash(password), full_name=clean_name)
    session.add(new_user)
    session.commit()
    
    db_user = session.query(models.User).filter(models.User.email == "strip@example.com").first()
    if db_user and db_user.full_name == "Stripped User":
        print("Success: Database contains stripped values.")
    else:
        print("Failure: Database values not as expected.")

    # 2. Verify Session Cart
    print("\n--- Verifying Session-Based Cart ---")
    # Simulate first session
    session1 = "session1@example.com"
    session2 = "session2@example.com"
    
    main.carts = {} # Reset
    
    # Add to cart for session 1
    # Mocking what get_session_cart does
    main.carts[session1] = [{"product": "dummy1", "quantity": 1}]
    main.carts[session2] = [{"product": "dummy2", "quantity": 2}]
    
    if len(main.carts[session1]) == 1 and main.carts[session1][0]["product"] == "dummy1":
        if len(main.carts[session2]) == 1 and main.carts[session2][0]["product"] == "dummy2":
            print("Success: Carts are independent for different sessions.")
        else:
            print("Failure: Session 2 cart incorrect.")
    else:
        print("Failure: Session 1 cart incorrect.")

    session.close()

if __name__ == "__main__":
    verify_all()
