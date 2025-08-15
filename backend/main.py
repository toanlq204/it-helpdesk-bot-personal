from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from openai_client import call_openai_api
from functions import get_faq_answer, create_ticket, get_software_info
from mock_data import ticket_data

app = FastAPI()


class UserMessage(BaseModel):
    message: str
    conversation_history: List[Dict[str, str]]


@app.post("/chat/")
async def chat(user_message: UserMessage):
    try:
        response = call_openai_api(
            user_message.message, user_message.conversation_history)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
