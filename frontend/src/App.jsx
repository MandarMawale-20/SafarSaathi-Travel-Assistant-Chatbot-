import { useState, useEffect } from 'react';
import './App.css';
import TravelChatbot from './components/chatbot'; // Correct import
import Login from './components/auth/Login.jsx';
import { auth } from './firebaseConfig';
import { onAuthStateChanged } from 'firebase/auth';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });

    // Cleanup subscription
    return () => unsubscribe();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Welcome to SafarSaathi</h1>
        {user && (
          <div className="user-info">
            <img src={user.photoURL} alt={user.displayName} className="avatar" />
            <span>Welcome, {user.displayName}</span>
            <button onClick={() => auth.signOut()} className="logout-btn">
              Logout
            </button>
          </div>
        )}
      </header>

      <main className="app-content">
        {user ? (
          <TravelChatbot user={user} />
        ) : (
          <div className="login-container">
            <h2>Welcome to SafarSaathi</h2>
            <p>Your AI-powered travel companion</p>
            <Login setUser={setUser} />
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>© 2025 SafarSaathi Travel Assistant</p>
      </footer>
    </div>
  );
}

export default App;
