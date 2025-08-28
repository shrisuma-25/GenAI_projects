# pip install "fastapi[all]" uvicorn
# uvicorn chatbot_backend:app --reload --port 8000

import time
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from dotenv import load_dotenv
import os

load_dotenv(override=True)
my_api_key = os.getenv("OPENAI_API_KEY")
print (f'Key is {my_api_key}')


client = OpenAI(api_key=my_api_key)
system_message = {
    "role": "system",
    "content": "You are a helpful assistant. Summarize the user input and return as a JSON string."
}
message_to_llm = [system_message]

class ChatApp:
    def ask_question(self, user_prompt: str) -> str:
        message_to_llm.append({"role": "user", "content": user_prompt})

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=message_to_llm,
            temperature=0.7,
            max_tokens=250,
        )
        reply = response.choices[0].message.content
        message_to_llm.append({"role": "assistant", "content": reply})
        return reply

# single chatbot instance
chatbot = ChatApp()

# --- FastAPI wrap (minimal) ---
app = FastAPI()

class AskRequest(BaseModel):
    prompt: str

class AskResponse(BaseModel):
    reply: str

@app.post("/ask_question", response_model=AskResponse)
def ask_question(req: AskRequest):
    try:
        reply = chatbot.ask_question(req.prompt)
        return AskResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))