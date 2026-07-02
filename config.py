import os

# ==========================
# BOT INFO
# ==========================

BOT_NAME = "TURNX AI Director"
BOT_VERSION = "V4"

# ==========================
# API KEYS
# ==========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

# ==========================
# IMAGE MODELS
# ==========================

IMAGE_MODELS = {

    "banana2": "Nano Banana Pro 2",

    "banana": "Nano Banana Pro",

    "chatgpt": "ChatGPT Image 2.0"

}

# ==========================
# VIDEO MODELS
# ==========================

VIDEO_MODELS = {

    "veo31": "Veo 3.1",

    "omni": "Omni",

    "seedance": "Seedance",

    "grok": "Grok"

}

# ==========================
# IMAGE → VIDEO
# ==========================

I2V_MODELS = VIDEO_MODELS.copy()

# ==========================
# FREE PLAN
# ==========================

FREE_GENERATIONS_PER_DAY = 5

# ==========================
# PREMIUM
# ==========================

PREMIUM_PRICE_STARS = 250

PREMIUM_DURATION_DAYS = 30

# ==========================
# STORAGE
# ==========================

DATABASE_FILE = "database.json"

MEMORY_FILE = "memory.json"

CHARACTER_FILE = "characters.json"

PREMIUM_FILE = "premium.json"

# ==========================
# DEFAULTS
# ==========================

DEFAULT_LANGUAGE = "English"

DEFAULT_COUNTRY = ""

DEFAULT_STYLE = "Photorealistic"
