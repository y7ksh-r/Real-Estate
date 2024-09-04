import firebase_admin
from firebase_admin import credentials, auth

# Use your Firebase project's credentials
cred = credentials.Certificate("path/to/your-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
