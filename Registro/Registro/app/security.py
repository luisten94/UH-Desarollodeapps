import hashlib
import secrets
from typing import Optional, Tuple

def pbkdf2_hash(password: str, salt: Optional[bytes] = None, iterations: int = 200_000) -> Tuple[bytes, bytes]:
    """Devuelve (hash, salt) usando PBKDF2-HMAC-SHA256."""
    if not isinstance(password, str):
        raise TypeError("password debe ser str")
    if salt is None:
        salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return dk, salt

def verify_password(password: str, stored_hash: bytes, salt: bytes, iterations: int = 200_000) -> bool:
    """Verifica contraseña contra hash+salt almacenados."""
    dk, _ = pbkdf2_hash(password, salt, iterations)
    return secrets.compare_digest(dk, stored_hash)
