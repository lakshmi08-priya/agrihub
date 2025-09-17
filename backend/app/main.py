from fastapi import FastAPI
from app.routers import predict, soil

app = FastAPI(title="Agriculture Backend")
app.include_router(predict.router, prefix="/predict")
app.include_router(soil.router, prefix="/soil")
