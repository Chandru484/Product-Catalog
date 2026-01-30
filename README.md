# LAKSHMI METAL WORKS - Product Catalog

A modern, fast, and elegant LAKSHMI METAL WORKS system with a shopping cart and admin management.

## 🚀 Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12)
- **Database**: SQLite with [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- **Authentication**: JWT & Passlib (Bcrypt) for secure Admin access
- **Frontend**: HTML5, Vanilla CSS, Jinja2 Templates
- **Styling**: Modern, premium design with micro-animations and responsive layouts

## ✨ Features

- **User Authentication**: Customers can create accounts, login, and logout.
- **Storefront**: Vibrant product grid with Rupee (₹) pricing and detail views.
- **Shopping Cart**: Real-time cart management and item tracking.
- **Manual Checkout**: Secure checkout view displaying bank details for customer transfers.
- **Admin Dashboard**: Full CRUD (Create, Read, Update, Delete) capabilities for the product catalog.
- **Dual Login**: A unified login page (`/login`) for both customers and admins.

## 🛠️ Project Structure

- `main.py`: Core API and route definitions.
- `models.py`: Database schemas for Products and Admins.
- `database.py`: SQLAlchemy connection and session management.
- `auth.py`: Security utilities for password hashing and tokens.
- `templates/`: Jinja2 HTML templates for all pages.
- `static/`: CSS styles and image assets.
- `init_db.py`: Database initialization and admin creation script.

## ⚙️ Setup & Installation

1. **Activate Virtual Environment**:
   ```powershell
   & .\.venv\Scripts\Activate.ps1
   ```

2. **Run Database Initialization**:
   ```powershell
   python init_db.py
   ```

3. **Start the Production Server**:
   ```powershell
   uvicorn main:app --reload
   ```

## 🔐 Credentials
- **Admin**: `admin` / `admin123`
- **Unified Login URL**: [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)

## 🌐 Deployment

### Deploying to Render (Recommended)

1. **GitHub**: Push your code to a GitHub repository.
2. **Render**:
   - Create a **New Web Service**.
   - Connect your repo.
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **Database**: Render's free tier has an ephemeral disk. To save products permanently, consider using Render's free **PostgreSQL** database and setting the `DATABASE_URL` environment variable in your service settings.
