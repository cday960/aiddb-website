import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
fernet = Fernet(str(os.getenv("FERNET_KEY")))


def encrypt_string(value: str) -> str:
    """
    Encrypts given str using Fernet key from env varaible
    """
    return fernet.encrypt(value.encode()).decode()


def decrypt_string(value: str) -> str:
    """
    Decrypts given str using Fernet key from env varaible
    """
    return fernet.decrypt(value.encode()).decode()
