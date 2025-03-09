import firebase_admin
from firebase_admin import credentials, auth
import os

# Check if Firebase is already initialized
def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # Look for the credentials file in the specified path
            cred_path = "core/chatbot-firebase-adminsdk.json"
            if not os.path.exists(cred_path):
                print(f"❌ Firebase credentials file not found at {cred_path}")
                return False
                
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin SDK initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Error initializing Firebase: {e}")
            return False
    return True

# Initialize Firebase on module import
firebase_initialized = initialize_firebase()

def verify_token(id_token):
    """Verify Firebase ID Token"""
    if not firebase_initialized:
        print("❌ Firebase not initialized, cannot verify token")
        return None
        
    try:
        decoded_token = auth.verify_id_token(id_token)
        print(f"✅ Token verified for user: {decoded_token.get('email', 'unknown')}")
        return decoded_token  # Contains user details like 'uid', 'email'
    except auth.ExpiredIdTokenError:
        print("❌ Token expired")
        return None
    except auth.InvalidIdTokenError:
        print("❌ Invalid token")
        return None
    except Exception as e:
        print(f"❌ Error verifying token: {e}")
        return None

def check_firebase_connection():
    """Check Firebase authentication by retrieving a user"""
    if not firebase_initialized:
        print("❌ Firebase not initialized, cannot check connection")
        return False
        
    try:
        user = auth.get_user_by_email("arnavmawale@gmail.com")
        print(f"✅ Successfully retrieved user: {user.uid}")
        return True
    except Exception as e:
        print(f"❌ Error fetching user: {e}")
        return False