from fastapi import FastAPI
from app.api.chat import router as chat_router

app = FastAPI(
    title="AI Red Team Lab",
    description="Staged AI system for security and red team testing",
    version="0.1"
)

app.include_router(chat_router, prefix="/chat")

@app.get("/")
def health_check():
    return {"status": "ok"}
