from fastapi import FastAPI
from app.api import chat

app = FastAPI(
    title="AI Red Team Lab",
    description="Staged AI system for security and red team testing",
    version="0.1"
)

app.include_router(chat.router)

@app.get("/")
def health_check():
    return {"status": "ok"}
