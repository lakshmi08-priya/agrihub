from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import SessionLocal, User
from app.auth import get_password_hash, create_access_token, verify_password
import os
from dotenv import load_dotenv

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH", "uploads")
os.makedirs(STORAGE_PATH, exist_ok=True)

# ------------------------------
# Create FastAPI app
# ------------------------------
app = FastAPI(title="Agriculture Backend API")

# ------------------------------
# Database dependency
# ------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------
# Pydantic models for requests
# ------------------------------
class UserCreate(BaseModel):
    username: str
    password: str

# ------------------------------
# Signup endpoint
# ------------------------------
@app.post("/signup", tags=["Auth"])
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

# ------------------------------
# Login endpoint
# ------------------------------
@app.post("/login", tags=["Auth"])
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# ------------------------------
# Predict endpoint (open for testing)
# ------------------------------
@app.post("/predict", tags=["Predict"])
async def predict(file: UploadFile = File(...)):
    """
    Temporarily open endpoint to test file uploads without authentication.
    Later, JWT auth can be added.
    """
    file_location = os.path.join(STORAGE_PATH, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"message": "File received ✅", "filename": file.filename}
