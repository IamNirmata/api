from typing import Optional
from pydantic import BaseModel

# In production, replace this with a secure database
fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": "$2b$12$..."
    }
}

class User(BaseModel):
    username: str
    hashed_password: str

def get_user(username: str) -> Optional[User]:
    user = fake_users_db.get(username)
    if user:
        return User(**user)
    return None
