from fastapi import APIRouter
from pydantic import BaseModel
import os
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    user_input: str

@router.post("/")
def chat(request: ChatRequest):
    with open("app/prompts/system_prompt.txt", "r") as f:
        system_prompt = f.read()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.user_input}
        ]
    )

    return {"response": response.choices[0].message.content}
