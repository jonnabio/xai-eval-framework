import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log detailed request/response info with a unique Request ID.
    """
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        # Attach request_id to request state for access in other components
        request.state.request_id = request_id
        
        logger.info(
            f"[{request_id}] Started {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else "unknown"
            }
        )
        
        start_time = time.time()
        try:
            response = await call_next(request)
            
            duration = time.time() - start_time
            logger.info(
                f"[{request_id}] Completed {response.status_code} in {duration:.3f}s",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "duration_ms": duration * 1000
                }
            )
            
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"[{request_id}] Failed with {type(e).__name__} in {duration:.3f}s",
                extra={
                    "request_id": request_id, 
                    "error": str(e)
                }
            )
            # Re-raise to be handled by exception handlers
            raise e
