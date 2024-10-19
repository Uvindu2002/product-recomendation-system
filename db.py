from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
import os

# Load MongoDB connection string from environment variable or use a default
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", 
    "mongodb+srv://wupu0327:wupu0327@users.zj7tl.mongodb.net/?retryWrites=true&w=majority&appName=userst"
)

# Initialize MongoDB client
client = None

# Function to connect to MongoDB
def connect_to_mongo():
    global client
    try:
        client = MongoClient(MONGO_CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=False)
        client.admin.command('ping')  # Check connection
        print("Connected to MongoDB!")
    except ConnectionFailure as e:
        print(f"Connection to MongoDB failed: {e}")
    except PyMongoError as e:
        print(f"An error occurred: {e}")

# Call the connect function
connect_to_mongo()

# Proceed only if the client is initialized successfully
if client:
    db = client['product_recommendation']  # Database name
    users_collection = db['users']  # Collection name

    # Function to save user info (username) in the database
    def save_user_info(email, username):
        """Save user info (username) in the database."""
        try:
            result = users_collection.update_one(
                {'email': email},  # Find the user by email
                {'$set': {'username': username}},  # Update or insert the username
                upsert=True  # Create the document if it doesn't exist
            )
            if result.upserted_id:
                print("New user created.")
            else:
                print("User info updated.")
            return True
        except PyMongoError as e:
            print(f"An error occurred while saving user info: {e}")
            return False

    # Function to retrieve user info (username) from the database
    def get_user_info(email):
        """Retrieve user info from the database."""
        try:
            user = users_collection.find_one({'email': email}, {'_id': 0, 'username': 1})
            if user:
                return {'username': user.get('username')}
            else:
                return None
        except PyMongoError as e:
            print(f"An error occurred while retrieving user info: {e}")
            return None

    # Function to save user preferences in the database
    def save_user_preferences(email, preferences):
        """Save user preferences in the database."""
        if client is None:
            print("Database connection is not available.")
            return False
        try:
            result = users_collection.update_one(
                {'email': email},
                {'$set': preferences},
                upsert=True
            )
            if result.upserted_id:
                print("New user preferences added.")
            else:
                print("User preferences updated.")
            return True
        except PyMongoError as e:
            print(f"An error occurred while saving user preferences: {e}")
            return False

    # Function to retrieve user preferences from the database
    def get_user_preferences(email):
        """Retrieve user preferences from the database."""
        if client is None:
            print("Database connection is not available.")
            return {}
        try:
            # Fetch user preferences based on the provided email
            user = users_collection.find_one({'email': email}, {'_id': 0, 'favorite_categories': 1, 'preferred_brands': 1})
            
            # If user is found, return their preferences; otherwise, return an empty dict
            if user:
                return {
                    'favorite_categories': user.get('favorite_categories', []),
                    'preferred_brands': user.get('preferred_brands', [])
                }
            else:
                return {'favorite_categories': [], 'preferred_brands': []}
        except PyMongoError as e:
            print(f"An error occurred while retrieving user preferences: {e}")
            return {}
else:
    print("Cannot proceed without a MongoDB client connection.")