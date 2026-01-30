# LAKSHMI METAL WORKS - Product Catalog

A modern, fast, and elegant product catalog system for LAKSHMI METAL WORKS, featuring a storefront for customers and a management dashboard for administrators.

## 🚀 Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12)
- **Database**: SQLite with [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- **Authentication**: Secure Admin access via Passlib (Bcrypt)
- **Frontend**: HTML5, Vanilla CSS (Modern & Responsive), Jinja2 Templates
- **Deployment**: Ready for [Render](https://render.com) or [Railway](https://railway.app)

## ✨ Features

- **Responsive Storefront**: Elegant product grid that works perfectly on Mobile, Tablet, and Desktop.
- **Search System**: Fast product searching with a clean, centered search interface.
- **Shopping Cart**: Real-time cart management for customers.
- **Admin Dashboard**: Secure panel to Add, Update, and Archive/Restore products.
- **Automatic Setup**: Database and Admin user are initialized automatically on first run.
- **Deployment Ready**: Includes `Procfile` and `requirements.txt` for easy cloud hosting.

## 🛠️ Project Structure

- `main.py`: Core application logic and API routes.
- `models.py`: Database schemas for Products, Users, and Admins.
- `database.py`: SQLAlchemy configuration and cloud database support.
- `auth.py`: Security utilities for password hashing.
- `init_db.py`: Database initialization script.
- `static/`: CSS styles and image assets.
- `templates/`: Jinja2 HTML templates for all pages.
- `requirements.txt`: Python dependencies.
- `Procfile`: Command for cloud hosting.

## ⚙️ Setup & Installation

1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd "Product Catalog"
   ```

2. **Create & Activate Virtual Environment**:
   ```powershell
   # Create the environment
   python -m venv .venv
   
   # Activate it (Windows)
   & .\.venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run Initialization**:
   The app initializes itself automatically, but you can run it manually:
   ```powershell
   python init_db.py
   ```

5. **Start the Development Server**:
   ```powershell
   uvicorn main:app --reload
   ```

6. **Access the App**:
   - Storefront: [http://127.0.0.1:8000/home](http://127.0.0.1:8000/home)
   - Login: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## ❓ Troubleshooting

If your teammate says the project "isn't working", check these common steps:

1. **Missing Dependencies**: Ensure they ran `pip install -r requirements.txt` inside an active virtual environment.
2. **Database Initialization**: If the app fails to start or data is missing, ask them to run `python init_db.py` to create the admin user and tables.
3. **Port Conflict**: If port 8000 is used by another app, they can run on a different port: `uvicorn main:app --reload --port 8080`.
4. **Python Version**: Ensure they are using Python 3.9 or higher (3.12 recommended).

## 🔐 Credentials
- **Default Admin**: `admin` / `admin123`

## 🌐 Deployment to Render

1. **Push to GitHub**: Push your latest code to your repository.
2. **New Web Service**:
   - Create a **New Web Service** on Render.
   - Connect your GitHub repo.
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

