from sqlalchemy import Column, Integer, String, Float
from .db import Base

# ---------------- USERS ----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


# ---------------- HEART ----------------
class HeartPrediction(Base):
    __tablename__ = "heart_predictions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    result = Column(String)
    probability = Column(Float)


# ---------------- FITNESS ----------------
class FitnessPrediction(Base):
    __tablename__ = "fitness_predictions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    result = Column(String)


# ---------------- FEEDBACK ----------------
class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    message = Column(String)

