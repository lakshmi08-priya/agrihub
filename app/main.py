from fastapi import FastAPI
from app.routers import predict, soil, disease

app = FastAPI()

app.include_router(predict.router, prefix="/ml", tags=["ML"])
app.include_router(soil.router, prefix="/soil", tags=["Soil"])
app.include_router(disease.router, prefix="/disease", tags=["Plant Disease"])
