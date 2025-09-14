from sqlalchemy import Column, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    feature1 = Column(Float, nullable=False)
    feature2 = Column(Float, nullable=False)
    feature3 = Column(Float, nullable=False)
    prediction = Column(Float, nullable=False)
