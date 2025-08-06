from util.crypto_utils import encrypt_string, decrypt_string


def test_encryption_decryption():
    original = "VerySecret!!!123"
    encrypted = encrypt_string(original)
    decrypted = decrypt_string(encrypted)
    assert decrypted == original
