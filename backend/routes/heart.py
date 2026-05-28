from fastapi import APIRouter, Depends
import joblib
import pandas as pd
from backend.database.db import SessionLocal
from backend.database.models import HeartPrediction
from backend.utils.dependencies import get_current_user

router = APIRouter()

# ✅ Load pipeline model (contains preprocessing + model)
model = joblib.load("backend/models/heart_model.pkl")


@router.post("/predict/heart")
def predict_heart(data: dict, user=Depends(get_current_user)):

    user_id = user["user_id"]

    db = SessionLocal()

    try:
        # ✅ No preprocessing needed
        df = pd.DataFrame([data])

        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1]

        # result = "High Risk" if pred == 1 else "Low Risk"
        # threshold = 0.55   # you can tune this

        # result = "High Risk" if prob >= threshold else "Low Risk"
        # 👇 ADD THIS
        if prob >= 0.7:
            result = "High Risk"
        elif prob >= 0.4:
            result = "Moderate Risk"
        else:
            result = "Low Risk"

        # Save to DB
        db.add(HeartPrediction(
            user_id=user_id,
            result=result,
            probability=float(prob)
        ))
        db.commit()

        return {
            "prediction": int(pred),
            "probability": float(round(prob, 3)),
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()