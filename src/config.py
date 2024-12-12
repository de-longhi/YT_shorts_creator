from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key
API_NINJAS_KEY = os.getenv("API_NINJAS_KEY")

# Verify that the API key is loaded (optional for debugging)
if not API_NINJAS_KEY:
    raise ValueError("API_NINJAS_KEY is not set. Please check your .env file.")
