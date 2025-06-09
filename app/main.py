from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routes
from app.database import engine, Base

app = FastAPI(title="Forex Observer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)
