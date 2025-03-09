from fastapi import FastAPI, HTTPException, Header
from gemini_api import get_gemini_response
from fastapi.middleware.cors import CORSMiddleware
from firebase_config import verify_token
from pydantic import BaseModel

app = FastAPI()

# Configure CORS - Make sure this is at the top
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenData(BaseModel):
    token: str

@app.get("/")
def home():
    return {"message": "Welcome to the Travel Assistant Chatbot API!"}

@app.post("/verify-token")
async def verify_firebase_token_endpoint(data: TokenData):
    """API to verify Firebase Authentication token"""
    decoded_token = verify_token(data.token)
    
    if decoded_token:
        return {"uid": decoded_token["uid"], "email": decoded_token.get("email")}
    
    raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/protected-route")
def protected_route(authorization: str = Header(None)):
    """ A protected route that requires a Firebase ID token """
    if not authorization:
        raise HTTPException(status_code=401, detail="No token provided")
    
    try:
        token = authorization.split(" ")[1]  # Extract token from "Bearer <token>"
        user_data = verify_token(token)
        
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        return {"message": "Welcome!", "user": user_data}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}")

@app.get("/chat")
def chat(prompt: str):
    response = get_gemini_response(prompt)
    return {"response": response}

# @app.on_event("startup")
# async def startup_event():
#     check_firebase_connection()

