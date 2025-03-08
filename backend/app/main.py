from fastapi import FastAPI
import gemini_api

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Google Gemini Chatbot API!"}

@app.get("/chat")
def chat(prompt: str):
    response = get_gemini_response(prompt)
    return {"response": response}
