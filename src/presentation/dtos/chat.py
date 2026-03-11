from typing import Optional
from pydantic import BaseModel

class SendMessageRequest(BaseModel):
    content: Optional[str] = None
