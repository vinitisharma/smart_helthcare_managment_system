from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.utils.auth_utils import decode_token

security = HTTPBearer()


# 👤 USER AUTH
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


# 🛠 ADMIN AUTH
def get_admin_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials
    payload = decode_token(token)

    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return payload