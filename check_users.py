from sqlalchemy.orm import sessionmaker
from database import engine
import models

def check_users():
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    users = session.query(models.User).all()
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"User: {user.email}, Name: {user.full_name}")
    session.close()

if __name__ == "__main__":
    check_users()
