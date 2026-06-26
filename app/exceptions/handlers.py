import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger("app.exceptions")

def setup_exception_handlers(app: FastAPI):
    """
    Registers exception handlers to standardise API error responses.
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation error: {exc.errors()} for path {request.url.path}")
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder({
                "success": False,
                "error": "Validation Error",
                "details": exc.errors()
            })
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database error occurred: {str(exc)} on path {request.url.path}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Database Error",
                "message": "A database transaction error occurred. Please contact the administrator."
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)} on path {request.url.path}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal Server Error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )
