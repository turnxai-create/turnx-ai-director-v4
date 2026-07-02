import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CONFIG = {
    "BOT_TOKEN": BOT_TOKEN,
    "GROQ_API_KEY": GROQ_API_KEY,
    "PORT": os.getenv("PORT", 5000),
}
