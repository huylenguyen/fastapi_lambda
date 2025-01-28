# standard imports
from contextlib import asynccontextmanager

# package imports
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from starlette.responses import JSONResponse

# local imports
from app.config import Settings
from app.routers.main import router as main_router
from app.routers.example import router as example_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown logic
    """
    pass  # startup logic
    yield
    pass  # shutdown logic


# initialise settings
settings = Settings.get_default_settings()

# define FastAPI application
app = FastAPI(
    lifespan=lifespan,
)


# add exception handler for error message logging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Ensure that all uncaught exceptions are returned as JSON responses.
    """

    # Extract the kind of exception
    formatted_exception = f"{exc.__class__.__name__}"

    # If there is more detail, add it to the response
    if str(exc):
        formatted_exception += f" - {str(exc)}"

    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {formatted_exception}"},
    )


# add routers
app.include_router(main_router)
app.include_router(example_router)

# add CORS middleware
if settings.CORS_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_allow_origins,
        allow_credentials=settings.CORS_allow_credentials,
        allow_methods=settings.CORS_allow_methods,
        allow_headers=settings.CORS_allow_headers,
    )


# Define the Lambda handler
handler = Mangum(app)
