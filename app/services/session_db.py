from flask import session, g
from util.custom_sql_class import SQLUtilities
from util.crypto_utils import encrypt_string, decrypt_string
from cryptography.fernet import InvalidToken


def get_db() -> SQLUtilities:
    if "db" in g:
        return g.db

    username = session.get("db_username")
    enc_pass = session.get("db_password")
    if not username or not enc_pass:
        raise RuntimeError("Not Authenticated")

    try:
        password = decrypt_string(enc_pass)
    except InvalidToken as e:
        raise RuntimeError("Invalid session token") from e

    g.db = SQLUtilities(
        server="aiddb",
        database="Columbia",
        username=username,
        password=password,
    )
    g.db.connect()
    return g.db
