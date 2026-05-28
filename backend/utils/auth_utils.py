from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=10)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        print("🔐 DECODING TOKEN:", token)   # ✅ ADD

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False}   # 🔥 ADD THIS
        )

        print("✅ TOKEN DECODED:", payload)  # ✅ ADD

        return payload

    except Exception as e:
        print("❌ TOKEN ERROR:", str(e))     # ✅ ADD
        return None