import secrets
import hashlib
from pwdlib import PasswordHash


hasher = PasswordHash.recommended() #Argon2


def hash_password(secret: str) -> str:
    return hasher.hash(secret)


def verify_password(secret: str, hashed_secret: str) -> bool:
    return hasher.verify(secret, hashed_secret)


def generate_auth_token() -> str:
    return secrets.token_hex()


def hash_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode()).hexdigest()