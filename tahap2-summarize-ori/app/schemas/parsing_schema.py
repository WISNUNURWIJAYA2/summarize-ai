from pydantic import BaseModel
from typing import Any


class ParsingResponse(BaseModel):
    filename: str
    parsed_data: Any    