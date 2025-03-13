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


