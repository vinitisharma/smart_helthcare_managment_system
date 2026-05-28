# from fastapi import APIRouter, Header
# from backend.database.db import SessionLocal
# from backend.database.models import HeartPrediction, FitnessPrediction, User, Feedback
# from backend.utils.auth_utils import decode_token

# router = APIRouter()


# # 🔐 Check admin
# def verify_admin(authorization):
#     token = authorization.split(" ")[1]
#     payload = decode_token(token)

#     if not payload or payload.get("role") != "admin":
#         return {"error": "Unauthorized"}

#     return payload


# # 📊 ADMIN DASHBOARD
# @router.get("/admin/dashboard")
# def admin_dashboard(authorization: str = Header(None, alias="Authorization")):

#     if not authorization:
#         return {"error": "Missing token"}

#     admin = verify_admin(authorization)
#     if not admin:
#         return {"error": "Unauthorized"}

#     db = SessionLocal()

#     total_users = db.query(User).count()
#     total_heart = db.query(HeartPrediction).count()
#     total_fitness = db.query(FitnessPrediction).count()

#     db.close()

#     return {
#         "total_users": total_users,
#         "total_heart_predictions": total_heart,
#         "total_fitness_predictions": total_fitness
#     }


# # ❤️ ALL HEART DATA
# @router.get("/admin/heart")
# def get_all_heart(authorization: str = Header(None)):

#     admin = verify_admin(authorization)
#     if not admin:
#         return {"error": "Unauthorized"}

#     db = SessionLocal()

#     data = db.query(HeartPrediction).all()

#     result = []
#     for d in data:
#         result.append({
#             "user_id": d.user_id,
#             "result": d.result,
#             "probability": d.probability
#         })

#     db.close()

#     return result


# # 🏋️ ALL FITNESS DATA
# @router.get("/admin/fitness")
# def get_all_fitness(authorization: str = Header(None)):

#     admin = verify_admin(authorization)
#     if not admin:
#         return {"error": "Unauthorized"}

#     db = SessionLocal()

#     data = db.query(FitnessPrediction).all()

#     result = []
#     for d in data:
#         result.append({
#             "user_id": d.user_id,
#             "result": d.result
#         })

#     db.close()

#     return result

# @router.get("/admin/feedback")
# def get_feedback(authorization: str = Header(None)):

#     admin = verify_admin(authorization)
#     if not admin:
#         return {"error": "Unauthorized"}

#     db = SessionLocal()

#     data = db.query(Feedback).all()

#     result = []
#     for d in data:
#         result.append({
#             "user_id": d.user_id,
#             "message": d.message
#         })

#     db.close()

#     print("Feedback data:", data)
    
#     return result


from fastapi import APIRouter, Depends
from backend.database.db import SessionLocal
from backend.database.models import HeartPrediction, FitnessPrediction, User, Feedback
from backend.utils.dependencies import get_admin_user

router = APIRouter()


# 📊 ADMIN DASHBOARD
@router.get("/admin/dashboard")
def admin_dashboard(admin=Depends(get_admin_user)):

    db = SessionLocal()

    total_users = db.query(User).count()
    heart_data = db.query(HeartPrediction).all()
    fitness_data = db.query(FitnessPrediction).all()

    # Heart breakdown
    high_risk = sum(1 for h in heart_data if h.result == "High Risk")
    low_risk = sum(1 for h in heart_data if h.result == "Low Risk")

    # Fitness breakdown
    fit = sum(1 for f in fitness_data if f.result == "Fit")
    moderate = sum(1 for f in fitness_data if f.result == "Moderate")
    unfit = sum(1 for f in fitness_data if f.result == "Unfit")

    db.close()

    return {
        "total_users": total_users,
        "total_heart": len(heart_data),
        "total_fitness": len(fitness_data),

        "heart_distribution": {
            "High Risk": high_risk,
            "Low Risk": low_risk
        },

        "fitness_distribution": {
            "Fit": fit,
            "Moderate": moderate,
            "Unfit": unfit
        }
    }


# ❤️ ALL HEART DATA
@router.get("/admin/heart")
def get_all_heart(admin=Depends(get_admin_user)):

    db = SessionLocal()

    data = db.query(HeartPrediction).all()

    result = [
        {
            "user_id": d.user_id,
            "result": d.result,
            "probability": d.probability
        }
        for d in data
    ]

    db.close()
    return result


# 🏋️ ALL FITNESS DATA
@router.get("/admin/fitness")
def get_all_fitness(admin=Depends(get_admin_user)):

    db = SessionLocal()

    data = db.query(FitnessPrediction).all()

    result = [
        {
            "user_id": d.user_id,
            "result": d.result
        }
        for d in data
    ]

    db.close()
    return result


# 💬 FEEDBACK
@router.get("/admin/feedback")
def get_feedback(admin=Depends(get_admin_user)):

    db = SessionLocal()

    data = db.query(Feedback).all()

    result = [
        {
            "user_id": d.user_id,
            "message": d.message
        }
        for d in data
    ]

    db.close()
    return result