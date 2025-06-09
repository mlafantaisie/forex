from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.data_fetcher import fetch_alpha_vantage_price, fetch_finnhub_quotes
from app.crud import insert_forex_price
from app import user_crud
from app import auth

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/signup")
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# Handle signup form submission
@router.post("/signup")
async def signup_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    existing_user = await user_crud.get_user_by_username(username)
    if existing_user:
        return RedirectResponse("/login", status_code=302)

    hashed_pw = hash_password(password)
    await user_crud.create_user(username, hashed_pw)
    return RedirectResponse("/login", status_code=302)

# Dependency to check login
async def get_current_user(request: Request):
    token = request.cookies.get("session_token")
    username = auth.verify_session_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username

# Login page
@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Handle login submission
@router.post("/login")
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await user_crud.get_user_by_username(username)
    if user and auth.verify_password(password, user.password_hash):
        response = RedirectResponse("/", status_code=302)
        token = auth.create_session_token(username)
        response.set_cookie("session_token", token, httponly=True)
        return response
    return RedirectResponse("/login", status_code=302)

# Logout
@router.post("/logout")
async def logout():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("session_token")
    return response

# Main dashboard
@router.get("/")
async def index(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@router.post("/admin/sync_tables")
# user=Depends(get_current_user)
async def sync_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return RedirectResponse("/", status_code=302)

# Alpha Vantage protected
@router.post("/fetch_alpha")
async def fetch_alpha(request: Request, base: str = Form(...), quote: str = Form(...), user=Depends(get_current_user)):
    price = await fetch_alpha_vantage_price(base, quote)
    if price:
        await insert_forex_price(base, quote, price, "AlphaVantage")
    return RedirectResponse("/", status_code=302)

# Finnhub protected
@router.post("/fetch_finnhub")
async def fetch_finnhub(request: Request, base: str = Form(...), user=Depends(get_current_user)):
    quotes = await fetch_finnhub_quotes(base)
    for quote_currency, price in quotes.items():
        await insert_forex_price(base, quote_currency, price, "Finnhub")
    return RedirectResponse("/", status_code=302)
