import React from "react";
import { auth, provider, signInWithPopup } from "../../firebaseConfig.js";

const Login = ({ setUser }) => {
  const handleGoogleSignIn = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const idToken = await result.user.getIdToken();
      setUser(result.user); // Store user info in state

      // Send token to FastAPI backend for verification
      const response = await fetch("http://127.0.0.1:8000/verify-token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: idToken }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("✅ Authenticated:", data);
      } else {
        console.error("❌ Authentication failed");
      }
    } catch (error) {
      console.error("❌ Login error:", error);
    }
  };

  return (
    <div>
      <button onClick={handleGoogleSignIn}>Sign in with Google</button>
    </div>
  );
};

export default Login;