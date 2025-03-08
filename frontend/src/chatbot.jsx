import { useState } from "react";
import axios from "axios";

const Chatbot = () => {
    const [prompt, setPrompt] = useState("");
    const [response, setResponse] = useState("");

    const sendMessage = async () => {
        try {
            const res = await axios.get(`http://127.0.0.1:8000/chat?prompt=${prompt}`);
            setResponse(res.data.response);
        } catch (error) {
            console.error("Error fetching response:", error);
            setResponse("Error connecting to chatbot.");
        }
    };

    return (
        <div className="p-4 max-w-md mx-auto bg-gray-100 rounded-lg shadow-md">
            <h2 className="text-xl font-bold">Chat with Gemini</h2>
            <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="w-full p-2 border rounded mt-2"
                placeholder="Ask me anything..."
            />
            <button
                onClick={sendMessage}
                className="w-full bg-blue-500 text-white p-2 rounded mt-2"
            >
                Send
            </button>
            {response && (
                <div className="mt-4 p-2 bg-white rounded shadow">
                    <strong>Response:</strong>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
};

export default Chatbot;
