"""
TURNX AI Director
Conversation State Manager
"""

from typing import Dict, Any

# In-memory state (replace with Redis/DB later if needed)
_USERS: Dict[int, Dict[str, Any]] = {}


def create_user(user_id: int):
    """Create a user record if it doesn't exist."""
    if user_id not in _USERS:
        _USERS[user_id] = {
            "state": None,
            "mode": None,
            "model": None,
            "idea": None,
            "character": None,
            "history": []
        }


def set_state(user_id: int, state: str):
    create_user(user_id)
    _USERS[user_id]["state"] = state


def get_state(user_id: int):
    create_user(user_id)
    return _USERS[user_id]["state"]


def clear_state(user_id: int):
    create_user(user_id)
    _USERS[user_id]["state"] = None


def set_mode(user_id: int, mode: str):
    create_user(user_id)
    _USERS[user_id]["mode"] = mode


def get_mode(user_id: int):
    create_user(user_id)
    return _USERS[user_id]["mode"]


def set_model(user_id: int, model: str):
    create_user(user_id)
    _USERS[user_id]["model"] = model


def get_model(user_id: int):
    create_user(user_id)
    return _USERS[user_id]["model"]


def set_idea(user_id: int, idea: str):
    create_user(user_id)
    _USERS[user_id]["idea"] = idea


def get_idea(user_id: int):
    create_user(user_id)
    return _USERS[user_id]["idea"]


def set_character(user_id: int, character: str):
    create_user(user_id)
    _USERS[user_id]["character"] = character


def get_character(user_id: int):
    create_user(user_id)
    return _USERS[user_id]["character"]


def add_history(user_id: int, item: str):
    create_user(user_id)
    _USERS[user_id]["history"].append(item)


def get_history(user_id: int):
    create_user(user_id)
    return _USERS[user_id]["history"]


def reset_user(user_id: int):
    _USERS[user_id] = {
        "state": None,
        "mode": None,
        "model": None,
        "idea": None,
        "character": None,
        "history": []
    }
