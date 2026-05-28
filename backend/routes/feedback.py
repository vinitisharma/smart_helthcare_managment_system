from fastapi import APIRouter, Header
from backend.database.db import SessionLocal
from backend.database.models import Feedback
from backend.utils.auth_utils import decode_token

router = APIRouter()


@router.post("/feedback")
def submit_feedback(data: dict, authorization: str = Header(None, alias="Authorization")):

    if not authorization:
        return {"error": "Missing token"}

    token = authorization.split(" ")[1]
    payload = decode_token(token)

    if not payload:
        return {"error": "Invalid token"}

    db = SessionLocal()

    feedback = Feedback(
        user_id=payload["user_id"],
        message=data.get("message")
    )

    db.add(feedback)
    db.commit()
    db.close()

    print("Saving feedback:", data)
    
    return {"message": "Feedback submitted"}


