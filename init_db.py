import database, models, auth

def init_admin():
    try:
        db = next(database.get_db())
        # Create an admin if not exists
        admin = db.query(models.Admin).filter(models.Admin.username == "admin").first()
        if not admin:
            print("Hashing password...")
            hashed_pw = auth.get_password_hash("admin123")
            print("Password hashed successfully.")
            new_admin = models.Admin(username="admin", hashed_password=hashed_pw)
            db.add(new_admin)
            db.commit()
            print("Admin user created: admin / admin123")
        else:
            print("Admin already exists.")
    except Exception as e:
        print(f"Error initializing admin: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=database.engine)
    init_admin()
