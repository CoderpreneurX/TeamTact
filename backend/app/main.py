# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.router import router as api_router

app = FastAPI(
    title="TeamTact API",
    version="1.0.0"
)

# CORS settings (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include versioned API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "🚀 TeamTact Backend is Live!"}
