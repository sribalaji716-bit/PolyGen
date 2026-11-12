from fastapi import FastAPI
from backend.api.prompt import router as prompt_router

app = FastAPI(
    title="PolyGen API",
    description="Generative Text-to-3D Asset Pipeline",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to PolyGen",
        "status": "Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(
    prompt_router,
    prefix="/api/prompt",
    tags=["Prompt Generation"]
)