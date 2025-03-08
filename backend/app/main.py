from fastapi import FastAPI
import gemini_api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Google Gemini Chatbot API!"}

@app.get("/chat")
def chat(prompt: str):
    response = get_gemini_response(prompt)
    return {"response": response}




app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
