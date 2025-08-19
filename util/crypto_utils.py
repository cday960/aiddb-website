import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


def load_fernet() -> Fernet:
    """
    Return a :class: cryptography.fernet.Fernet instance
    """

    key = os.getenv("FERNET_KEY")
    if not key:
        key = Fernet.generate_key().decode()
        os.environ["FERNET_KEY"] = key

    try:
        return Fernet(key)
    except ValueError as e:
        raise ValueError("FERNET_KEY must be 32 url-safe base64-encoded bytes") from e


fernet = load_fernet()


def encrypt_string(value: str | None) -> str:
    """
    Encrypts given str using Fernet key from env varaible
    """
    if value is None:
        raise AttributeError("String is of type None, could not encrypt")
    return fernet.encrypt(value.encode()).decode()


def decrypt_string(value: str) -> str:
    """
    Decrypts given str using Fernet key from env varaible
    """
    return fernet.decrypt(value.encode()).decode()
