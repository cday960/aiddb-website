import os
import datetime
import pylibmc
import redis
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("APP_SECRET")
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=5)
    SESSION_PERMANENT = False
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True


class RedisConfig(Config):
    REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url(REDIS_URL, decode_responses=False)
    SESSION_KEY_PREFIX = "sess:"  # avoid key collisions
    SESSION_USE_SIGNER = True  # adds hmac sig to cookie session id
    SESSION_REFRESH_EACH_REQUEST = True  # refersh ttl when active


class MemcachedConfig(Config):
    SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), "flask_session")
    SESSION_TYPE = "memcached"
    SESSION_MEMCACHED = pylibmc.Client(["127.0.0.1"], binary=True)
    SESSION_PERMANENT = False


class DevConfig(Config):
    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_SECURE = False
    SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), ".flask_session")
