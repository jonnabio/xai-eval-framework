"""
Custom exception handlers for the API.

Provides consistent error responses across the application.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
):
    """
    Handle Pydantic validation errors.
    
    Returns 400 Bad Request with error details.
    """
    logger.warning(f"Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "timestamp": datetime.now().isoformat()
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions.
    
    Returns 500 Internal Server Error.
    """
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error_type": type(exc).__name__,
            "timestamp": datetime.now().isoformat()
        }
    )

async def not_found_handler(request: Request, exc):
    """
    Handle 404 Not Found errors.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "Resource not found",
            "path": str(request.url),
            "timestamp": datetime.now().isoformat()
        }
    )
