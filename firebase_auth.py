import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('DATABASEURL')
})

auth = auth
db = db.reference()

def signup(data):
    """
    Signs up a new user by creating an account with Firebase Authentication and
    storing user details (excluding password) in the Firebase Realtime Database.

    Args:
        data (dict): A dictionary containing 'email', 'password', 'role', and other user details.

    Returns:
        bool: True if the signup was successful, False otherwise.
    """
    if not "@" in data['email'] or not "." in data['email']:
        print("Invalid email format.")
        return

    if len(data['password']) < 8:
        print("Password must be at least 8 characters long.")
        return

    if data['role'].lower() not in ["mentor", "peer"]:
        print("Invalid role. Please enter 'mentor' or 'peer'.")
        return

    try:
        # Create user with Firebase Authentication
        user = auth.create_user(
            email=data['email'],
            password=data['password']
        )
        uid = user.uid  # Get the user's UID

        # Store user data in Realtime Database
        del data['password']
        db.child("users").child(uid).set(data)

        print("Successfully signed up.")
        return True

    except firebase_admin.exceptions.AuthError as e:
        print(f"Authentication error: {e}")
        return False
    except Exception as e:
        print(f"Error during signup: {e}")
        return False

def login(data):
    """
    Logs in a user by verifying their email and password using Firebase Authentication.

    Args:
        data (dict): A dictionary containing 'email' and 'password' of the user.

    Returns:
        bool: True if login is successful, False if authentication fails.
    """
    try:
        user = auth.sign_in_with_email_and_password(
            email=data['email'],
            password=data['password']
        )
        print("Successfully logged in.")
        return True

    except firebase_admin.exceptions.AuthError:
        print("Invalid email or password.")
        return False

def available_mentors():
    """
    Retrieves all users with the role 'mentor' from the Firebase Realtime Database.

    Returns:
        dict: A dictionary containing all users with the role 'mentor'.
    """
    mentors = db.child("users").order_by_child("role").equal_to('mentor').get()
    return mentors

def available_peers(expertise=None):
    """
    Retrieves all users with the role 'peer' from the Firebase Realtime Database.
    Optionally filters peers by their expertise.

    Args:
        expertise (str, optional): The expertise field to filter peers by. Defaults to None.

    Returns:
        dict: A dictionary containing all peers, or peers filtered by expertise if provided.
    """
    if expertise is None:
        peers = db.child("users").order_by_child("role").equal_to('peer').get()
    else:
        peers = db.child("users").order_by_child("role").equal_to('peer').order_by_child('expertise').equal_to(expertise).get()
    return dict(peers)

# data = {"name": "Micas", "email": "kkk123@gmail.com", "password": "Micasa@123", "role": "mentor"}

# print(available_mentors())
