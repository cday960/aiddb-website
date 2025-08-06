import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
fernet = Fernet(str(os.getenv("FERNET_KEY")))


def encrypt_string(value: str | None) -> str:
    """
    Encrypts given str using Fernet key from env varaible
    """
    if not value:
        raise AttributeError("String is of type None, could not encrypt")
    return fernet.encrypt(value.encode()).decode()


def decrypt_string(value: str) -> str:
    """
    Decrypts given str using Fernet key from env varaible
    """
    return fernet.decrypt(value.encode()).decode()
