from fastapi import APIRouter, Header, Request, Depends
from backend.utils.dependencies import get_current_user
import joblib
import pandas as pd
from backend.database.db import SessionLocal
from backend.database.models import FitnessPrediction
from backend.utils.auth_utils import decode_token

router = APIRouter()

# Load model
model = joblib.load("backend/models/fitness_model.pkl")



@router.post("/predict/fitness")
def predict_fitness(data: dict, user=Depends(get_current_user)):

    user_id = user["user_id"]

    db = SessionLocal()

    try:
        columns = [
            'age','gender','height','weight','body_fat',
            'diastolic','systolic','gripForce',
            'flexibility','situps','jump'
        ]

        df = pd.DataFrame([data])

        for col in columns:
            if col not in df:
                df[col] = 0

        df = df[columns].astype(float)

        prediction = model.predict(df)[0]

        db.add(FitnessPrediction(
            user_id=user_id,
            result=prediction
        ))
        db.commit()

        return {"prediction": prediction}

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return {"error": str(e)}

    finally:
        db.close()