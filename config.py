# config.py
# TURNX AI Director V4 - Production Config

import os

# ==========================================================
# CORE ENV VARIABLES
# ==========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Default Groq model (can be overridden in ai.py)
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# ==========================================================
# APP CONFIG WRAPPER (USED BY app.py)
# ==========================================================

CONFIG = {
    "BOT_TOKEN": BOT_TOKEN,
    "GROQ_API_KEY": GROQ_API_KEY,
    "GROQ_MODEL": GROQ_MODEL,
    "PORT": int(os.getenv("PORT", "5000")),
}

# ==========================================================
# VALIDATION (FAIL FAST IN PRODUCTION)
# ==========================================================

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment variables")
