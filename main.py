from fastapi import FastAPI
from app.api.routes import predict

app = FastAPI()

# Register routes
app.include_router(predict.router, prefix="/api/v1", tags=["Prediction"])

@app.get("/")
def root():
    return {"message": "AgroLens API is running!"}
