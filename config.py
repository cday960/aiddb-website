import os
import datetime
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("APP_SECRET")
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=5)
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True  # Adds HMAC sig to session cookie
    SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), "flask_session")
    WTF_CSRF_ENABLED = True
