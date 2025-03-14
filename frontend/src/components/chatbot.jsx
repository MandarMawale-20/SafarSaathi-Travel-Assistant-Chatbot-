import { useState } from "react";

const TravelChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState("");
  const [userId] = useState(() => Math.random().toString(36).substr(2, 9));

  const sendMessage = async (message) => {
    if (!message.trim()) return; // Prevent empty messages

    // Add user message to chat
    setMessages((prevMessages) => [...prevMessages, { user: message }]);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, message }),
      });

      const data = await response.json();
      console.log("API Response:", data); // ✅ Debugging print

      // Add bot response if available
      if (data.reply) {
        setMessages((prevMessages) => [...prevMessages, { bot: data.reply }]);
      }

      // ✅ Check if flights exist and add them as cards inside chatbox
      if (data.flights && Array.isArray(data.flights.flights)) {
        console.log("Flights received:", data.flights.flights);

        // Add flights as a single message containing multiple cards
        setMessages((prevMessages) => [
          ...prevMessages,
          { flights: data.flights.flights },
        ]);
      }

      // Clear user input field after sending
      setUserMessage("");
    } catch (error) {
      console.error("Error:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { bot: "Sorry, something went wrong. Please try again later." },
      ]);
    }
  };

  return (
    <div style={{ width: "400px", margin: "auto", textAlign: "center" }}>
      <h2>Travel Assistant</h2>

      {/* Chat Messages */}
      <div
        style={{
          height: "400px",
          overflowY: "auto",
          border: "1px solid #ccc",
          padding: "10px",
          marginBottom: "10px",
          backgroundColor: "#4D5D53",
          color: "#fff",
        }}
      >
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.user ? "right" : "left" }}>
            {msg.user && (
              <p>
                <strong>You:</strong> {msg.user}
              </p>
            )}
            {msg.bot && (
              <p>
                <strong>Bot:</strong> {msg.bot}
              </p>
            )}
            {msg.flights && (
              <div>
                <h3>✈️ Available Flights</h3>
                {msg.flights.map((flight, idx) => (
                  <div
                    key={idx}
                    style={{
                      border: "1px solid #ddd",
                      borderRadius: "8px",
                      padding: "10px",
                      marginBottom: "10px",
                      backgroundColor: "#7CB9E8",
                      display: "flex",
                      alignItems: "center",
                    }}
                  >
                    <img
                      src={flight.logo}
                      alt={flight.airline}
                      style={{ width: "40px", height: "40px", marginRight: "10px" }}
                    />
                    <div>
                      <strong>
                        Airline Name ✈️ :{flight.airline} ({flight.iata_code})
                      </strong>
                      <p>Price💰: ₹{flight.price} </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Text Input for User Messages */}
      <input
        type="text"
        value={userMessage}
        onChange={(e) => setUserMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") sendMessage(userMessage);
        }}
        placeholder="Type your question..."
        style={{ width: "80%", padding: "5px", marginTop: "10px" }}
      />
      <button
        onClick={() => sendMessage(userMessage)}
        style={{ padding: "5px 10px", marginLeft: "5px" }}
      >
        Send
      </button>

      {/* Quick Action Buttons */}
      <div style={{ marginTop: "10px" }}>
        <button onClick={() => sendMessage("1")}>Plan a Trip</button>
        <button onClick={() => sendMessage("2")}>Find a Hotel</button>
        <button onClick={() => sendMessage("3")}>Get Directions</button>
        <button onClick={() => sendMessage("4")}>Find Attractions</button>
      </div>
    </div>
  );
};

export default TravelChatbot;
