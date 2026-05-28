from fastapi import APIRouter
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from backend.database.db import SessionLocal
from backend.database.models import User
from backend.utils.auth_utils import create_token

load_dotenv()

router = APIRouter()

class LoginSchema(BaseModel):
    email: str
    password: str

class RegisterSchema(BaseModel):
    name: str
    email: str
    password: str


# 📝 REGISTER
@router.post("/register")
def register(data: RegisterSchema):

    db = SessionLocal()

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        return {"error": "User already exists"}

    new_user = User(
        name=data.name,
        email=data.email,
        password=data.password
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "User created successfully"}


# 🔐 USER LOGIN
@router.post("/login")
def login(data: LoginSchema):

    db = SessionLocal()

    user = db.query(User).filter(User.email == data.email).first()

    if not user or user.password != data.password:
        return {"error": "Invalid credentials"}

    token = create_token({
        "user_id": user.id,
        "role": "user"
    })

    print("🟢 USER TOKEN:", token)

    return {
        "access_token": token,
        "role": "user"
    }


# 🔐 ADMIN LOGIN
@router.post("/admin/login")
def admin_login(data: LoginSchema):

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if data.email == admin_email and data.password == admin_password:

        token = create_token({
            "user_id": 0,
            "role": "admin"
        })

        print("🟢 ADMIN TOKEN:", token)

        return {
            "access_token": token,
            "role": "admin"
        }

    return {"error": "Invalid admin credentials"}