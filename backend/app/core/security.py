import bcrypt
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from app.core.config import settings

ALGORITHM = "HS256"

def create_access_token(
    subject: Union[str, Any], roles: list[str], permissions: list[str], expires_delta: timedelta = None, secret_key: str = settings.SECRET_KEY
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    
    # Using the standard .NET role claim URI for Blazor compatibility
    # Multiple roles and permissions are added as lists
    to_encode = {
        "exp": expire, 
        "sub": str(subject),
        "http://schemas.microsoft.com/ws/2008/06/identity/claims/role": roles,
        "permissions": permissions
    }
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed one using direct bcrypt.
    Compatible with passlib's bcrypt format.
    """
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """
    Hash a password using direct bcrypt.
    """
    pwd_bytes = password.encode('utf-8')
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')
