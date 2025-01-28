# package imports
from pydantic import BaseModel


class ExampleRequest(BaseModel):
    a: float
    b: float


class ExampleResponse(BaseModel):
    result: float
