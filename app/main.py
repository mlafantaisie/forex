import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from app.data_fetcher import fetch_finnhub_rsi

load_dotenv()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "defaultsecret"))

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    env_user = os.getenv("APP_USERNAME")
    env_pass = os.getenv("APP_PASSWORD")
    if username == env_user and password == env_pass:
        request.session["user"] = username
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if "user" not in request.session:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("dashboard.html", {"request": request, "stock_data": None})

@app.post("/dashboard", response_class=HTMLResponse)
async def dashboard_post(request: Request, ticker: str = Form(...)):
    if "user" not in request.session:
        return RedirectResponse(url="/login")

    rsi_data = await fetch_finnhub_rsi(ticker.upper())

    stock_data = {
        "ticker": ticker.upper(),
        "rsi": rsi_data.get("rsi", "N/A"),
        "date": rsi_data.get("timestamp", "N/A")
    }

    return templates.TemplateResponse("dashboard.html", {"request": request, "stock_data": stock_data})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")
