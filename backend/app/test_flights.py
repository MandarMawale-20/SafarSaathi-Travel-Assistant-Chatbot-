import requests
import os
import json

# Replace with your actual API key
BOOKING_COM_API_KEY = os.getenv("BOOKING_COM_API_KEY")
BOOKING_COM_API_URL = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"

def get_all_flight_details(from_location, to_location, depart_date, return_date, num_people):
    """Fetches flight details (airline name, logo, price) from the Booking.com API."""
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
    response = requests.get(BOOKING_COM_API_URL, headers=headers, params=params)
    data=response.json()
    return data

# import requests
# import json
# def extract_flight_details(response_data):
#     airlines = response_data["data"]["aggregation"]["airlines"]
#     for airline in airlines:
#         name = airline["name"]
#         logo_url = airline["logoUrl"]
#         price=airline["minPrice"]["units"]
#         print(f"Airline: {name}, Logo: {logo_url},Price:{price}")
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
            return "No flights found. Please check your details."

        airlines = data["data"]["aggregation"]["airlines"]
        flight_info = []

        for airline in airlines[:5]:  # Get top 5 results
            flight_info.append(
                f"✈️ **{airline['name']}** ({airline['iataCode']})\n"
                f"💰 Price: {airline['minPrice']['units']}\n"
            )

        return "**Top 5 Flight Options:**\n\n" + "\n".join(flight_info)
    except Exception as e:
        return f"Error fetching flights: {str(e)}"



from_location = "JFK.AIRPORT"  # Example: New York JFK
to_location = "LHR.AIRPORT"    # Example: London Heathrow
depart_date = "2025-04-10"
return_date = "2025-04-20"
num_people = 1

# Run the function and print results
response=get_flight_details(from_location, to_location, depart_date, return_date, num_people)
print(response)
# Example Usage
# extract_flight_details(response)

# from fastapi import FastAPI, HTTPException, Header
# from fastapi.middleware.cors import CORSMiddleware
# import google.generativeai as genai
# from firebase_config import verify_token
# from pydantic import BaseModel
# import random
# import os

# app = FastAPI()

# # Allow frontend requests
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow frontend origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Configure Gemini API
# api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("GOOGLE_GEMINI_API_KEY is not set in environment variables.")

# genai.configure(api_key=api_key)
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Store user session data
# user_sessions = {}

# class ChatRequest(BaseModel):
#     user_id: str
#     message: str

# class TokenData(BaseModel):
#     token: str

# # Predefined structured question flow
# QUESTION_FLOW = {
#     "start": [
#         "Hello! How can I assist you today?",
#         "Choose an option by entering a number:",
#         "1️⃣ Travel itinerary",
#         "2️⃣ Find a hotel",
#         "3️⃣ Get directions",
#         "4️⃣ Things to do"
#     ],
#     "itinerary": [
#         "Where are you traveling to?",
#         "How long is your trip?",
#         "What type of activities do you prefer?",
#         "What is your travel start date? (YYYY-MM-DD)"
#     ],
#     "hotel": [
#         "Which city?",
#         "What is your budget?",
#         "Hotel, hostel, or apartment?"
#     ],
#     "directions": [
#         "Starting location?",
#         "Destination?",
#         "Preferred transport: train, bus, flight?"
#     ],
#     "attractions": [
#         "Which city?",
#         "What type of activity: food, museums, parks, shopping?",
#         "Solo, family, or group trip?"
#     ]
# }

# QUESTION_MAPPING = {
#     "1": "itinerary",
#     "2": "hotel",
#     "3": "directions",
#     "4": "attractions"
# }

# GREETING_RESPONSES = [
#     "Hello! How can I assist you today?",
#     "Hi there! How can I help with your travel plans?",
#     "Hey! What can I do for you today?"
# ]

# @app.post("/chat")
# def chat(request: ChatRequest):
#     """Handles user messages and guides structured question flow."""
#     user_id = request.user_id
#     user_input = request.message.lower().strip()

#     print(f"User {user_id} sent: {request.message}")

#     # Handle greetings
#     if user_input in ["hi", "hello", "hey"]:
#         return {"reply": random.choice(GREETING_RESPONSES) + "\n\n" + "\n".join(QUESTION_FLOW["start"][1:])}

#     # Handle numeric selections (1-4)
#     if user_input in QUESTION_MAPPING:
#         user_choice = QUESTION_MAPPING[user_input]
#         user_sessions[user_id] = {"step": user_choice, "responses": []}
#         user_sessions[user_id]["index"] = 0  # Start at first question
#         return {"reply": QUESTION_FLOW[user_choice][0]}

#     # Check if user is in an active session
#     session = user_sessions.get(user_id)
#     if session:
#         step = session["step"]
#         responses = session["responses"]
#         index = session["index"]

#         # Store user response
#         responses.append(request.message)

#         # Move to next question
#         if index < len(QUESTION_FLOW[step]) - 1:
#             user_sessions[user_id]["index"] += 1
#             return {"reply": QUESTION_FLOW[step][index + 1]}
#         else:
#             # Generate AI response using all gathered inputs
#             structured_prompt = (
#                 f"User is planning a {step}.\n"
#                 f"Here are their responses in order:\n"
#                 f"{responses}\n"
#                 f"Provide a detailed, relevant travel response based on this."
#             )
#             try:
#                 ai_response = model.generate_content(structured_prompt)
                
#                 # Reset session after AI response
#                 del user_sessions[user_id]

#                 return {"reply": ai_response.text}
#             except Exception as e:
#                 raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")

#     # If input is unknown, show available options again
#     return {"reply": "\n".join(QUESTION_FLOW["start"])}

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




