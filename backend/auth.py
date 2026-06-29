import bcrypt
from .database import create_user, get_user_by_username, get_user_by_email, get_user_by_id

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def register_user(username: str, email: str, name: str, password: str, referral_code: str | None = None) -> dict:
    if len(password) < 6:
        return {"success": False, "error": "Password must be at least 6 characters"}
    if get_user_by_username(username):
        return {"success": False, "error": "Username already exists"}
    if get_user_by_email(email):
        return {"success": False, "error": "Email already registered"}

    referred_by = None
    if referral_code:
        from .database import get_user_by_referral_code
        referrer = get_user_by_referral_code(referral_code)
        if referrer:
            referred_by = referrer["id"]

    hashed = hash_password(password)
    user_id = create_user(username, email, name, hashed, referred_by)
    if user_id is None:
        return {"success": False, "error": "Registration failed"}

    user = get_user_by_id(user_id)
    if user and user.get("email"):
        from utils.email_sender import send_welcome_email
        send_welcome_email(user["email"], user["name"], user.get("referral_code"), "ar")

    return {"success": True, "user_id": user_id}

def authenticate_user(username: str, password: str) -> dict | None:
    user = get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user
