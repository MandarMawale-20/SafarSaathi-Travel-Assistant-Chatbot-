import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyCG1oOe7Z1ee4ff_uhgxuxpA0-3TiiD9IQ",
    authDomain: "travel-assistant-chatbot.firebaseapp.com",
    projectId: "travel-assistant-chatbot",
    storageBucket: "travel-assistant-chatbot.firebasestorage.app",
    messagingSenderId: "1020134871165",
    appId: "1:1020134871165:web:1e10281b404b07fb08e114",
    measurementId: "G-R1XVZ9S6BS"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Export the necessary Firebase components
export { auth, provider, signInWithPopup };