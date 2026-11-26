
from fastapi import APIRouter

from schemas import ChatRequest, ChatResponse
from services.llm_service import generate_response

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):

    answer = await generate_response(request.message)

    return ChatResponse(
        user_message=request.message,
        response=answer,
        model="qwen3:0.6b"
    )
