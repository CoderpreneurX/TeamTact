"""
Custom Exceptions for the application
"""

from fastapi import Request
from fastapi.responses import JSONResponse


class JSONException(Exception):
    """
    Custom exception for handling JSON errors in the FastAPI application.

    Attributes:
        message (str): Human-readable error message.
        status_code (int): HTTP status code to return with the response.
    """

    def __init__(self, message: str | dict[str, str], status_code: int = 400):
        self.message = message
        self.status_code = status_code


async def json_exception_handler(_: Request, exc: JSONException):
    """
    Asynchronous exception handler for JSONException.

    Returns a JSON response with the error message and HTTP status code.

    Args:
        exc (JSONException): The exception instance raised.

    Returns:
        JSONResponse: A FastAPI JSONResponse with 'success' and 'message' keys.
    """
    return JSONResponse(
        status_code=exc.status_code, content={"success": False, "message": exc.message}
    )
