# package imports
from fastapi import APIRouter

# local imports
from app.schemas import ExampleRequest, ExampleResponse


router = APIRouter()


@router.post(path="/example", response_model=ExampleResponse)
async def example_route(request: ExampleRequest) -> ExampleResponse:
    """
    An example of a POST route
    """
    return {"result": request.a + request.b}
