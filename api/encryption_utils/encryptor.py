import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def derive_key(password, salt):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    return kdf.derive(password.encode())

def encrypt_file(content, password):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(content) + padder.finalize()
    encrypted_content = encryptor.update(padded_data) + encryptor.finalize()

    return salt + iv + encrypted_content

def decrypt_file(encrypted_data, password):
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    encrypted_content = encrypted_data[32:]
    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        padded_content = decryptor.update(encrypted_content) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        content = unpadder.update(padded_content) + unpadder.finalize()
        return content
    except Exception as e:
        raise ValueError("Decryption failed, possibly due to an incorrect password or corrupted data.")
