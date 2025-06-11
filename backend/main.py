"""
This is the main module that has the App instance and its configuration
"""

from typing import cast
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ExceptionHandler

from app.api.router import router as api_router
from app.core.exceptions import JSONException, json_exception_handler

app = FastAPI(title="TeamTact API", version="1.0.0")

app.add_exception_handler(JSONException, cast(ExceptionHandler, json_exception_handler))

# CORS settings (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Change to specific domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include versioned API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    """
    Sample root API
    """
    return {"message": "🚀 TeamTact Backend is Live!"}
