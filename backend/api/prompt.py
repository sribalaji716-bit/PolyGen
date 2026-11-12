from fastapi import APIRouter
from backend.schemas.prompt import PromptRequest

router = APIRouter()


@router.post("/generate")
def generate_asset(request: PromptRequest):
    return {
        "status": "success",
        "message": "Prompt received successfully",
        "prompt": request.prompt,
        "generation_status": "pending"
    }