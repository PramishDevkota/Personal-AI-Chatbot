from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
        description="Message sent by the user"
    )


class ChatResponse(BaseModel):
    user_message: str
    response: str
    model: str