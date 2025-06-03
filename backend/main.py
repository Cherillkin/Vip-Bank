from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from . import models, database
from .routes import router

app = FastAPI(
    title="VIP Банк API",
    description="API для управления VIP-клиентами и операциями",
    version="1.0.0"
)

models.Base.metadata.create_all(bind=database.engine)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
