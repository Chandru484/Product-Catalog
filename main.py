from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, File, UploadFile
import shutil
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, database, auth
from database import engine, get_db
import os

app = FastAPI()

# Initialize DB and Admin on startup
@app.on_event("startup")
async def startup_event():
    models.Base.metadata.create_all(bind=engine)
    from init_db import init_admin
    init_admin()

# Mount static files
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Mock Cart for simplicity (in-memory for this session)
# In a real app, use sessions or a database table
cart = []

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    # If already logged in, go to home
    if request.cookies.get("user_session") or request.cookies.get("admin_session"):
        return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, q: str = None, db: Session = Depends(get_db)):
    if not request.cookies.get("user_session") and not request.cookies.get("admin_session"):
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    query = db.query(models.Product).filter(models.Product.is_active == True)
    if q:
        query = query.filter(models.Product.name.contains(q))
    
    products = query.all()
    return templates.TemplateResponse("index.html", {"request": request, "products": products, "cart_count": len(cart), "search_query": q})

@app.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    if not request.cookies.get("user_session") and not request.cookies.get("admin_session"):
        return RedirectResponse(url="/")
    
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("product.html", {"request": request, "product": product, "cart_count": len(cart)})

@app.post("/add-to-cart/{product_id}")
async def add_to_cart(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        # Check if product already in cart
        for item in cart:
            if item["product"].id == product_id:
                item["quantity"] += 1
                break
        else:
            cart.append({"product": product, "quantity": 1})
    return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/remove-from-cart/{product_id}")
async def remove_from_cart(product_id: int):
    global cart
    cart = [item for item in cart if item["product"].id != product_id]
    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/update-cart-quantity/{product_id}")
async def update_cart_quantity(product_id: int, action: str = Form(...)):
    for item in cart:
        if item["product"].id == product_id:
            if action == "increase":
                item["quantity"] += 1
            elif action == "decrease":
                item["quantity"] -= 1
                if item["quantity"] <= 0:
                    cart.remove(item)
            break
    return RedirectResponse(url="/cart", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request):
    if not request.cookies.get("user_session") and not request.cookies.get("admin_session"):
        return RedirectResponse(url="/")
    total = sum(item["product"].rate * item["quantity"] for item in cart if item["product"].rate)
    return templates.TemplateResponse("cart.html", {"request": request, "cart": cart, "total": total})

@app.get("/checkout", response_class=HTMLResponse)
async def checkout(request: Request):
    if not request.cookies.get("user_session") and not request.cookies.get("admin_session"):
        return RedirectResponse(url="/")
    return templates.TemplateResponse("checkout.html", {"request": request})

@app.post("/user/login")
async def user_login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or password"})
    
    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user_session", value=user.email)
    return response

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup(request: Request, email: str = Form(...), password: str = Form(...), full_name: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Email already registered"})
    
    new_user = models.User(email=email, hashed_password=auth.get_password_hash(password), full_name=full_name)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("user_session")
    response.delete_cookie("admin_session")
    return response

@app.get("/change-password", response_class=HTMLResponse)
async def change_password_page(request: Request):
    if not request.cookies.get("user_session") and not request.cookies.get("admin_session"):
        return RedirectResponse(url="/")
    return templates.TemplateResponse("change_password.html", {"request": request})

@app.post("/change-password")
async def change_password(
    request: Request, 
    current_password: str = Form(...), 
    new_password: str = Form(...), 
    db: Session = Depends(get_db)
):
    user_email = request.cookies.get("user_session")
    admin_session = request.cookies.get("admin_session")
    
    if user_email:
        user = db.query(models.User).filter(models.User.email == user_email).first()
        if not user or not auth.verify_password(current_password, user.hashed_password):
            return templates.TemplateResponse("change_password.html", {"request": request, "error": "Invalid current password"})
        user.hashed_password = auth.get_password_hash(new_password)
        db.commit()
        return templates.TemplateResponse("change_password.html", {"request": request, "success": "Password updated successfully!"})
    
    elif admin_session == "authenticated":
        admin = db.query(models.Admin).filter(models.Admin.username == "admin").first()
        if not admin or not auth.verify_password(current_password, admin.hashed_password):
            return templates.TemplateResponse("change_password.html", {"request": request, "error": "Invalid current password"})
        admin.hashed_password = auth.get_password_hash(new_password)
        db.commit()
        return templates.TemplateResponse("change_password.html", {"request": request, "success": "Password updated successfully!"})
    
    return RedirectResponse(url="/")

# Old routes redirected to /
@app.get("/login")
async def old_login():
    return RedirectResponse(url="/")

@app.get("/admin/login")
async def old_admin_login():
    return RedirectResponse(url="/")

@app.post("/admin/login")
async def admin_login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.username == username).first()
    if not admin or not auth.verify_password(password, admin.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    response = RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="admin_session", value="authenticated")
    return response

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    if request.cookies.get("admin_session") != "authenticated":
        return RedirectResponse(url="/")
    products = db.query(models.Product).filter(models.Product.is_active == True).all()
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "products": products})

@app.post("/admin/add-product")
async def add_product(
    name: str = Form(...), 
    description: str = Form(...), 
    qty: int = Form(1),
    rate: float = Form(...), 
    image_file: UploadFile = File(None),
    back_image_file: UploadFile = File(None),
    image_url: str = Form(None), 
    back_image_url: str = Form(None),
    weight: float = Form(None),
    rc_rate_kg_invoice: float = Form(None),
    machining_cost_invoice: float = Form(None),
    rate_piece_invoice: float = Form(None),
    rc_rate_kg_no_invoice: float = Form(None),
    machining_cost_no_invoice: float = Form(None),
    rate_piece_no_invoice: float = Form(None),
    selling_price_invoice: float = Form(None),
    selling_price_no_invoice: float = Form(None),
    db: Session = Depends(get_db)
):
    # Handle Image Uploads
    final_image_url = image_url
    if image_file and image_file.filename:
        file_path = f"static/images/{name}_{image_file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
        final_image_url = f"/{file_path}"

    final_back_url = back_image_url
    if back_image_file and back_image_file.filename:
        file_path = f"static/images/{name}_back_{back_image_file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(back_image_file.file, buffer)
        final_back_url = f"/{file_path}"

    new_product = models.Product(
        name=name, 
        description=description, 
        qty=qty,
        rate=rate, 
        image_url=final_image_url,
        back_image_url=final_back_url,
        weight=weight,
        rc_rate_kg_invoice=rc_rate_kg_invoice,
        machining_cost_invoice=machining_cost_invoice,
        rate_piece_invoice=rate_piece_invoice,
        rc_rate_kg_no_invoice=rc_rate_kg_no_invoice,
        machining_cost_no_invoice=machining_cost_no_invoice,
        rate_piece_no_invoice=rate_piece_no_invoice,
        selling_price_invoice=selling_price_invoice,
        selling_price_no_invoice=selling_price_no_invoice
    )
    db.add(new_product)
    db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/admin/delete-product/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        product.is_active = False
        db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/admin/archive", response_class=HTMLResponse)
async def admin_archive(request: Request, db: Session = Depends(get_db)):
    if request.cookies.get("admin_session") != "authenticated":
        return RedirectResponse(url="/")
    products = db.query(models.Product).filter(models.Product.is_active == False).all()
    return templates.TemplateResponse("admin_archive.html", {"request": request, "products": products})

@app.post("/admin/restore-product/{product_id}")
async def restore_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        product.is_active = True
        db.commit()
    return RedirectResponse(url="/admin/archive", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/admin/edit-product/{product_id}", response_class=HTMLResponse)
async def edit_product_page(request: Request, product_id: int, db: Session = Depends(get_db)):
    if request.cookies.get("admin_session") != "authenticated":
        return RedirectResponse(url="/")
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("edit_product.html", {"request": request, "product": product})

@app.post("/admin/update-product/{product_id}")
async def update_product(
    product_id: int,
    name: str = Form(...),
    description: str = Form(...),
    qty: int = Form(1),
    rate: float = Form(...),
    image_file: UploadFile = File(None),
    back_image_file: UploadFile = File(None),
    image_url: str = Form(None),
    back_image_url: str = Form(None),
    weight: float = Form(None),
    rc_rate_kg_invoice: float = Form(None),
    machining_cost_invoice: float = Form(None),
    rate_piece_invoice: float = Form(None),
    rc_rate_kg_no_invoice: float = Form(None),
    machining_cost_no_invoice: float = Form(None),
    rate_piece_no_invoice: float = Form(None),
    selling_price_invoice: float = Form(None),
    selling_price_no_invoice: float = Form(None),
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        product.name = name
        product.description = description
        product.qty = qty
        product.rate = rate
        
        # Handle Image Uploads
        if image_file and image_file.filename:
            file_path = f"static/images/{name}_{image_file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image_file.file, buffer)
            product.image_url = f"/{file_path}"
        elif image_url:
            product.image_url = image_url

        if back_image_file and back_image_file.filename:
            file_path = f"static/images/{name}_back_{back_image_file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(back_image_file.file, buffer)
            product.back_image_url = f"/{file_path}"
        elif back_image_url:
            product.back_image_url = back_image_url

        product.weight = weight
        product.rc_rate_kg_invoice = rc_rate_kg_invoice
        product.machining_cost_invoice = machining_cost_invoice
        product.rate_piece_invoice = rate_piece_invoice
        product.rc_rate_kg_no_invoice = rc_rate_kg_no_invoice
        product.machining_cost_no_invoice = machining_cost_no_invoice
        product.rate_piece_no_invoice = rate_piece_no_invoice
        product.selling_price_invoice = selling_price_invoice
        product.selling_price_no_invoice = selling_price_no_invoice
        db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_303_SEE_OTHER)
