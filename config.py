import os
import datetime
import pylibmc
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("APP_SECRET")
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=5)
    SESSION_TYPE = "memcached"
    SESSION_MEMCACHED = pylibmc.Client(["127.0.0.1"], binary=True)
    SESSION_PERMANENT = False
    # SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), "flask_session")
    WTF_CSRF_ENABLED = True
