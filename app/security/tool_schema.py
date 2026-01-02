from pydantic import BaseModel, Field
from typing import Literal

class ToolInvocation(BaseModel):
    tool: Literal["generate_report"]
    content: str = Field(..., min_length=1, max_length=5000)
