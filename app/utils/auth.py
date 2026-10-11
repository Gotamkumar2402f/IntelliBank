# Simple in-memory user store (for demo)
# In production: use database + hashed passwords

USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "name": "Administrator",
    },
    "user": {
        "password": "user123",
        "role": "user",
        "name": "Bank User",
    },
}


def authenticate(username: str, password: str):
    """Return user dict if valid, else None."""
    user = USERS.get(username)
    if user and user["password"] == password:
        return {
            "username": username,
            "role": user["role"],
            "name": user["name"],
        }
    return None


def is_admin(user):
    return user and user.get("role") == "admin"