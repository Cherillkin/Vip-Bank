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
