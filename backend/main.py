from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.db import engine
from backend.database import models
from backend.routes import heart, fitness, auth, dashboard, admin, feedback

app = FastAPI()

app.include_router(dashboard.router)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")

app.include_router(admin.router)

app.include_router(feedback.router)

# CORS (important for Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router, prefix="/auth")
app.include_router(heart.router)
app.include_router(fitness.router)


@app.get("/")
def home():
    return {"message": "API is running"}