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
    <div style={{ 
      width: "500px", 
      margin: "auto", 
      textAlign: "center",
      fontFamily: "Arial, sans-serif",
      boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
      borderRadius: "12px",
      overflow: "hidden"
    }}>
     
      {/* Chat Header */}
      <div style={{
        padding: "12px",
        backgroundColor: "#34495e",
        color: "#fff",
        fontSize: "18px",
        fontWeight: "bold"
      }}>
        Travel Assistant
      </div>
     
      {/* Chat Messages */}
      <div
        style={{
          height: "400px",
          overflowY: "auto",
          border: "1px solid #ddd",
          padding: "15px",
          marginBottom: "10px",
          backgroundColor: "#4D5D53",
          color: "#fff",
          textAlign: "left"
        }}
      >
        {messages.map((msg, index) => (
          <div key={index} style={{ 
            marginBottom: "12px",
            textAlign: msg.user ? "right" : "left" 
          }}>
            {msg.user && (
              <div style={{
                backgroundColor: "#3498db",
                color: "#fff",
                borderRadius: "18px 18px 0 18px",
                padding: "10px 15px",
                display: "inline-block",
                maxWidth: "80%"
              }}>
                <strong>You:</strong> {msg.user}
              </div>
            )}
            {msg.bot && (
              <div style={{
                backgroundColor: "#2c3e50",
                color: "#fff",
                borderRadius: "18px 18px 18px 0",
                padding: "10px 15px",
                display: "inline-block",
                maxWidth: "80%"
              }}>
                <strong>Bot:</strong> {msg.bot}
              </div>
            )}
            {msg.flights && (
              <div style={{
                width: "100%",
                backgroundColor: "#2c3e50",
                borderRadius: "8px",
                padding: "10px",
                marginBottom: "10px",
              }}>
                <h3 style={{
                  margin: "0 0 10px 0",
                  fontSize: "16px",
                  borderBottom: "1px solid #7CB9E8",
                  paddingBottom: "5px"
                }}>✈️ Available Flights</h3>
                {msg.flights.map((flight, idx) => (
                  <div
                    key={idx}
                    style={{
                      border: "1px solid #7CB9E8",
                      borderRadius: "8px",
                      padding: "12px",
                      marginBottom: "10px",
                      backgroundColor: "#7CB9E8",
                      display: "flex",
                      alignItems: "center",
                      transition: "transform 0.2s",
                      cursor: "pointer"
                    }}
                    onMouseOver={(e) => e.currentTarget.style.transform = "translateY(-2px)"}
                    onMouseOut={(e) => e.currentTarget.style.transform = "translateY(0)"}
                  >
                    <img
                      src={flight.logo}
                      alt={flight.airline}
                      style={{ 
                        width: "40px", 
                        height: "40px", 
                        marginRight: "15px",
                        borderRadius: "50%",
                        backgroundColor: "#fff",
                        padding: "5px"
                      }}
                    />
                    <div style={{ textAlign: "left" }}>
                      <strong style={{ fontSize: "15px" }}>
                        {flight.airline} ({flight.iata_code}) ✈️
                      </strong>
                      <p style={{ 
                        margin: "5px 0 0 0",
                        color: "#ffffff",
                        fontWeight: "bold"  
                      }}>Price💰: ₹{flight.price} </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Text Input for User Messages */}
      <div style={{ display: "flex", padding: "0 10px 10px 10px" }}>
        <input
          type="text"
          value={userMessage}
          onChange={(e) => setUserMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage(userMessage);
          }}
          placeholder="Type your question..."
          style={{ 
            width: "80%", 
            padding: "10px", 
            border: "1px solid #ddd",
            borderRadius: "20px 0 0 20px",
            outline: "none"
          }}
        />
        <button
          onClick={() => sendMessage(userMessage)}
          style={{ 
            padding: "10px 15px", 
            backgroundColor: "#34495e", 
            color: "#fff",
            border: "none",
            borderRadius: "0 20px 20px 0",
            cursor: "pointer"
          }}
        >
          Send
        </button>
      </div>

      {/* Quick Action Buttons */}
      <div style={{ 
        marginTop: "5px", 
        display: "flex", 
        justifyContent: "space-between",
        padding: "0 10px 15px 10px"
      }}>
        <button onClick={() => sendMessage("1")} style={{ 
          padding: "8px 12px", 
          backgroundColor: "#7CB9E8", 
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
          flex: "1",
          margin: "0 5px"
        }}>Plan a Trip</button>
        <button onClick={() => sendMessage("2")} style={{ 
          padding: "8px 12px", 
          backgroundColor: "#7CB9E8", 
          color: "#fff", 
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
          flex: "1",
          margin: "0 5px"
        }}>Find a Hotel</button>
        <button onClick={() => sendMessage("3")} style={{ 
          padding: "8px 12px", 
          backgroundColor: "#7CB9E8", 
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
          flex: "1",
          margin: "0 5px"
        }}>Get Directions</button>
        <button onClick={() => sendMessage("4")} style={{ 
          padding: "8px 12px", 
          backgroundColor: "#7CB9E8", 
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
          flex: "1",
          margin: "0 5px"
        }}>Find Attractions</button>
      </div>
    </div>
  );

};

export default TravelChatbot;
