import pytest
from util.crypto_utils import encrypt_string, decrypt_string


def test_encryption_decryption():
    original = "VerySecret!!!123"
    encrypted = encrypt_string(original)
    decrypted = decrypt_string(encrypted)
    assert decrypted == original


def test_encrypt_none_string_raises():
    with pytest.raises(AttributeError):
        encrypt_string(None)
