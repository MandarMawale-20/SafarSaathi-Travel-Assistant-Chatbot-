from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from firebase_config import verify_token
from pydantic import BaseModel
import random
import os
import requests

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_GEMINI_API_KEY is not set in environment variables.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Store user session data
user_sessions = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

class TokenData(BaseModel):
    token: str

# Predefined structured question flow (Including flight booking)
QUESTION_FLOW = {
    "start": [
        "Hello! How can I assist you today?",
        "Choose an option by entering a number:",
        "1️⃣ Travel itinerary",
        "2️⃣ Find a hotel",
        "3️⃣ Get directions",
        "4️⃣ Things to do"
    ],
    "itinerary": [
        "Where are you traveling to?",
        "How long is your trip?",
        "What type of activities do you prefer?",
        "Which city are you flying from?",
        "What is your departure date? (YYYY-MM-DD)",
        "What is your return date? (YYYY-MM-DD)",
        "How many people are traveling?"
    ],
    "hotel": [
        "Which city?",
        "What is your budget?",
        "Hotel, hostel, or apartment?"
    ],
    "directions": [
        "Starting location?",
        "Destination?",
        "Preferred transport: train, bus, flight?"
    ],
    "attractions": [
        "Which city?",
        "What type of activity: food, museums, parks, shopping?",
        "Solo, family, or group trip?"
    ]
}

QUESTION_MAPPING = {
    "1": "itinerary",
    "2": "hotel",
    "3": "directions",
    "4": "attractions"
}

GREETING_RESPONSES = [
    "Hello! How can I assist you today?",
    "Hi there! How can I help with your travel plans?",
    "Hey! What can I do for you today?"
]

BOOKING_COM_API_KEY = os.getenv("BOOKING_COM_API_KEY")
BOOKING_COM_API_URL = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"

@app.post("/chat")
def chat(request: ChatRequest):
    """Handles user messages and guides structured question flow."""
    user_id = request.user_id
    user_input = request.message.lower().strip()

    print(f"User {user_id} sent: {request.message}")

    # Handle greetings
    if user_input in ["hi", "hello", "hey"]:
        return {"reply": random.choice(GREETING_RESPONSES) + "\n\n" + "\n".join(QUESTION_FLOW["start"][1:])}

    # Handle numeric selections (1-4)
    if user_input in QUESTION_MAPPING:
        user_choice = QUESTION_MAPPING[user_input]
        user_sessions[user_id] = {"step": user_choice, "responses": [], "index": 0}
        user_sessions[user_id]["index"] = 0 
        return {"reply": QUESTION_FLOW[user_choice][0]}

    # Check if user is in an active session
    session = user_sessions.get(user_id)
    if session:
        step = session["step"]
        responses = session["responses"]
        index = session["index"]

        # Store user response
        responses.append(request.message)

        # Move to the next question
        if index < len(QUESTION_FLOW[step]) - 1:
            user_sessions[user_id]["index"] += 1
            return {"reply": QUESTION_FLOW[step][index + 1]}

        # **Itinerary Handling (Includes Flights)**
        elif step == "itinerary":
            (
                travel_destination,
                trip_length,
                activity_type,
                from_location,
                depart_date,
                return_date,
                num_people
            ) = responses

            structured_prompt = (
                f"Create a {trip_length}-day itinerary for {travel_destination}. "
                f"The user prefers {activity_type} activities."
            )

            try:
                ai_response = model.generate_content(structured_prompt).text
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")

            # Fetch flight details
            flight_response = get_flight_details(from_location, travel_destination, depart_date, return_date, int(num_people))

           
            del user_sessions[user_id]
            # return {"reply": f"{ai_response}\n"}
            return {"reply": ai_response, "flights": flight_response}
        
        structured_prompt = (
            f"User is planning a {step}.\n"
            f"Here are their responses in order:\n"
            f"{responses}\n"
            f"Provide a detailed, relevant travel response based on this."
        )
        try:
            ai_response = model.generate_content(structured_prompt)
    
            del user_sessions[user_id]  # 🔥 Reset session after AI response
            return {"reply": ai_response.text}
        except Exception as e:
            return {"reply": f"AI generation error: {str(e)}"}
    # If input is unknown, show available options again
    return {"reply": "\n".join(QUESTION_FLOW["start"])}

def get_flight_details(from_location, to_location, depart_date, return_date, num_people):
    """Calls the Booking.com API to fetch flight details."""
    headers = {
        "x-rapidapi-key": BOOKING_COM_API_KEY,
        "x-rapidapi-host": "booking-com15.p.rapidapi.com"
    }
    params = {
        "fromId": from_location,
        "toId": to_location,
        "departDate": depart_date,
        "returnDate": return_date,
        "adults": num_people,
        "sort": "BEST",
        "cabinClass": "ECONOMY",
        "currency_code": "INR"
    }

    try:
        response = requests.get(BOOKING_COM_API_URL, headers=headers, params=params)
        data = response.json()
        
        if "data" not in data or "aggregation" not in data["data"]:
            return {"error": "No flights found. Please check your details."}

        airlines = data["data"]["aggregation"]["airlines"]
        flight_cards = []

        for airline in airlines[:5]:  # Get top 5 results
            flight_cards.append({
                "airline": airline["name"],
                "iata_code": airline["iataCode"],
                "logo": airline["logoUrl"],
                "price": airline["minPrice"]["units"],
                
            })

        return {"flights": flight_cards}

    except Exception as e:
        return {"error": f"Error fetching flights: {str(e)}"}



# @app.get("/")
# def home():
#     """Home endpoint to confirm API is running."""
#     return {"message": "Welcome to the Travel Assistant Chatbot API!"}

# @app.post("/verify-token")
# async def verify_firebase_token_endpoint(data: TokenData):
#     """API to verify Firebase Authentication token."""
#     decoded_token = verify_token(data.token)
    
#     if decoded_token:
#         return {"uid": decoded_token["uid"], "email": decoded_token.get("email")}
    
#     raise HTTPException(status_code=401, detail="Invalid or expired token")

# @app.get("/protected-route")
# def protected_route(authorization: str = Header(None)):
#     """A protected route that requires a Firebase ID token."""
#     if not authorization:
#         raise HTTPException(status_code=401, detail="No token provided")
    
#     try:
#         token = authorization.split(" ")[1]  # Extract token from "Bearer <token>"
#         user_data = verify_token(token)
        
#         if not user_data:
#             raise HTTPException(status_code=401, detail="Invalid or expired token")
        
#         return {"message": "Welcome!", "user": user_data}
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}")





