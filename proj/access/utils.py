import os

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password:str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def admin_emails():
    """Emails allowed to hold the admin role, read from the ADMIN_EMAILS env var
    (comma-separated). Comparison is case-insensitive."""
    raw = os.getenv("ADMIN_EMAILS", "")
    return {e.strip().lower() for e in raw.split(",") if e.strip()}


def role_for_email(email: str) -> str:
    """Resolve the role an email should have: 'admin' if it is in the
    ADMIN_EMAILS allowlist, otherwise 'user'."""
    return "admin" if email.lower() in admin_emails() else "user"
