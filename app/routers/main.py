# package imports
from fastapi import APIRouter

# local imports
from app.schemas import GreetingResponse


router = APIRouter()


@router.get(path="/", response_model=GreetingResponse)
async def main_route() -> GreetingResponse:
    """
    Ping the top-level path
    """
    return {"message": "Hello World!"}
