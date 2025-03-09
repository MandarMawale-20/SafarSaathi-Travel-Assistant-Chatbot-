import { useState, useEffect, useRef } from 'react'
import './Chatbot.css'

const Chatbot = ({ user }) => {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm SafarSaathi, your travel assistant. How can I help you today?", sender: 'bot' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    
    if (!input.trim()) return
    
    // Add user message
    const userMessage = { text: input, sender: 'user' }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)
    
    try {
      // Get user's Firebase ID token
      const idToken = await user.getIdToken()
      
      // Send request to backend with authentication
      const response = await fetch(`http://127.0.0.1:8000/chat?prompt=${encodeURIComponent(input)}`, {
        headers: {
          'Authorization': `Bearer ${idToken}`
        }
      })
      
      const data = await response.json()
      
      // Add bot response
      setMessages(prev => [...prev, { text: data.response, sender: 'bot' }])
    } catch (error) {
      console.error('Error fetching response:', error)
      setMessages(prev => [...prev, { 
        text: "Sorry, I'm having trouble connecting to my brain right now. Please try again later.", 
        sender: 'bot',
        error: true
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h2>Travel Assistant</h2>
      </div>
      
      <div className="messages">
        {messages.map((message, index) => (
          <div 
            key={index} 
            className={`message ${message.sender} ${message.error ? 'error' : ''}`}
          >
            {message.text}
          </div>
        ))}
        {loading && (
          <div className="message bot loading">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={sendMessage} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about destinations, itineraries, travel tips..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? '...' : 'Send'}
        </button>
      </form>
      
      <div className="suggestion-chips">
        <button onClick={() => setInput("Recommend places to visit in Bali")}>
          Bali recommendations
        </button>
        <button onClick={() => setInput("What should I pack for a winter trip to Switzerland?")}>
          Winter packing list
        </button>
        <button onClick={() => setInput("Create a 5-day itinerary for Tokyo")}>
          Tokyo itinerary
        </button>
      </div>
    </div>
  )
}

export default Chatbot