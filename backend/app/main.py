from fastapi import FastAPI
from .routers import soil, predict

app = FastAPI()

# include routers
app.include_router(soil.router, prefix="/soil", tags=["Soil"])
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])

@app.get("/")
def root():
    return {"message": "AgroLens API is running 🚀"}
