# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import google.generativeai as genai
# import os
# import random
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # Allow frontend requests
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Debugging: Allow all origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Configure Gemini API
# api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("GEMINI_API_KEY is not set in environment variables.")

# genai.configure(api_key=api_key)
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Store user session data
# user_sessions = {}

# class ChatRequest(BaseModel):
#     user_id: str
#     message: str

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
#         "What type of activities do you prefer?"
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
#     user_id = request.user_id
#     user_input = request.message.lower().strip()

#     print(f"User {user_id} sent: {request.message}")

#     # Handle greetings
#     if user_input in ["hi", "hello", "hey"]:
#         return {"reply": random.choice(GREETING_RESPONSES) + "\n\n" + "\n".join(QUESTION_FLOW["start"][1:])}

#     # Handle numeric selections (1-4)
#     if user_input in QUESTION_MAPPING:
#         user_choice = QUESTION_MAPPING[user_input]
#         user_sessions[user_id] = user_choice
#         user_sessions[user_id + "_index"] = 0  # Start at first question
#         return {"reply": QUESTION_FLOW[user_choice][0]}

#     # Continue structured flow
#     user_step = user_sessions.get(user_id, "start")

#     if user_step in QUESTION_FLOW:
#         questions = QUESTION_FLOW[user_step]
#         current_index = user_sessions.get(user_id + "_index", 0)

#         if current_index < len(questions) - 1:
#             user_sessions[user_id + "_index"] = current_index + 1
#             return {"reply": questions[current_index + 1]}
#         else:
#             # Generate AI response after last question
#             structured_prompt = (
#                 f"Provide a detailed but concise travel guide based on the user's choices:\n"
#                 f"User step: {user_step}\n"
#                 f"User message: {request.message}\n"
#                 f"Focus on real locations, travel advice, and useful tips."
#             )
#             try:
#                 ai_response = model.generate_content(structured_prompt)
                
#                 # Reset user session after AI response
#                 del user_sessions[user_id]
#                 del user_sessions[user_id + "_index"]

#                 return {"reply": ai_response.text}
#             except Exception as e:
#                 raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")

#     # If input is unknown, show available options again
#     return {"reply": "\n".join(QUESTION_FLOW["start"])}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Store user session data
user_sessions = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

# Predefined structured question flow
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
        "What type of activities do you prefer?"
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

@app.post("/chat")
def chat(request: ChatRequest):
    user_id = request.user_id
    user_input = request.message.lower().strip()

    print(f"User {user_id} sent: {request.message}")

    # Handle greetings
    if user_input in ["hi", "hello", "hey"]:
        return {"reply": random.choice(GREETING_RESPONSES) + "\n\n" + "\n".join(QUESTION_FLOW["start"][1:])}

    # Handle numeric selections (1-4)
    if user_input in QUESTION_MAPPING:
        user_choice = QUESTION_MAPPING[user_input]
        user_sessions[user_id] = {"step": user_choice, "responses": []}
        user_sessions[user_id]["index"] = 0  # Start at first question
        return {"reply": QUESTION_FLOW[user_choice][0]}

    # Check if user is in an active session
    session = user_sessions.get(user_id)
    if session:
        step = session["step"]
        responses = session["responses"]
        index = session["index"]

        # Store user response
        responses.append(request.message)

        # Move to next question
        if index < len(QUESTION_FLOW[step]) - 1:
            user_sessions[user_id]["index"] += 1
            return {"reply": QUESTION_FLOW[step][index + 1]}
        else:
            # Generate AI response using all gathered inputs
            structured_prompt = (
                f"User is planning a {step}.\n"
                f"Here are their responses in order:\n"
                f"{responses}\n"
                f"Provide a detailed, relevant travel response based on this."
            )
            try:
                ai_response = model.generate_content(structured_prompt)
                
                # Reset session after AI response
                del user_sessions[user_id]

                return {"reply": ai_response.text}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")

    # If input is unknown, show available options again
    return {"reply": "\n".join(QUESTION_FLOW["start"])}
