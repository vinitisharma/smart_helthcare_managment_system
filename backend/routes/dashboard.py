from fastapi import APIRouter, Header
from backend.database.db import SessionLocal
from backend.database.models import HeartPrediction, FitnessPrediction
from backend.utils.auth_utils import decode_token

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(authorization: str = Header(None, alias="Authorization")):

    token = authorization.split(" ")[1]
    payload = decode_token(token)

    if not payload:
        return {"error": "Invalid or expired token"}

    user_id = payload["user_id"]

    db = SessionLocal()

    heart = db.query(HeartPrediction)\
        .filter(HeartPrediction.user_id == user_id)\
        .order_by(HeartPrediction.id.desc()).first()

    fitness = db.query(FitnessPrediction)\
        .filter(FitnessPrediction.user_id == user_id)\
        .order_by(FitnessPrediction.id.desc()).first()
    db.close()
    return {
        "heart": heart.result if heart else None,
        "heart_prob": heart.probability if heart else None,
        "fitness": fitness.result if fitness else None,

        # NEW: history
        "heart_history": [
            {"id": h.id, "prob": h.probability}
            for h in db.query(HeartPrediction)
            .filter(HeartPrediction.user_id == user_id)
            .order_by(HeartPrediction.id.asc()).all()
        ],

        "fitness_history": [
            {"id": f.id, "result": f.result}
            for f in db.query(FitnessPrediction)
            .filter(FitnessPrediction.user_id == user_id)
            .order_by(FitnessPrediction.id.asc()).all()
        ]
    }