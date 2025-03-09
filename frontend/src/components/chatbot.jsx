import { useState } from "react";

const TravelChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState("");
  const [userId] = useState(() => Math.random().toString(36).substr(2, 9));

  const sendMessage = async (message) => {
    if (!message.trim()) return; // Prevent empty messages

    const userMsg = { user: message };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, message }),
      });

      const data = await response.json();
      const botMsg = { bot: data.reply };
      setMessages((prev) => [...prev, botMsg]);

      // Clear user input field after sending
      setUserMessage("");
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
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
          height: "300px",
          overflowY: "auto",
          border: "1px solid #ccc",
          padding: "10px",
          marginBottom: "10px",
          backgroundColor: "#4D5D53"
        
        }}
      >
        {messages.map((msg, index) => (
          <p key={index} style={{ textAlign: msg.user ? "right" : "left" }}>
            <strong>{msg.user ? "You:" : "Bot:"}</strong> {msg.user || msg.bot}
          </p>
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
