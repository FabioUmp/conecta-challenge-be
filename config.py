import os
from dotenv import load_dotenv


load_dotenv()

class Config:
   
    CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE")
    SCOPES = os.getenv("SCOPES").split(",") 
    API_SERVICE_NAME = os.getenv("API_SERVICE_NAME")
    API_VERSION = os.getenv("API_VERSION")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
