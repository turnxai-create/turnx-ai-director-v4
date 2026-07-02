# app.py
# TURNX AI Director V4 - Render Safe Flask Entry

from __future__ import annotations

import os
import logging
from flask import Flask, jsonify

from config import CONFIG
from telegram import register as register_telegram_routes

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("turnx")

# ==========================================================
# FLASK APP
# ==========================================================

app = Flask(__name__)

# Register Telegram webhook routes
register_telegram_routes(app)

# ==========================================================
# HEALTH CHECK ROUTE
# ==========================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "status": "online",
            "service": "TURNX AI Director V4",
        }
    )

# ==========================================================
# STARTUP (FLASK 3 SAFE)
# ==========================================================

def init_app() -> None:
    """
    Safe startup initializer for Render / Gunicorn.
    Flask 3.x does NOT support before_first_request.
    """
    logger.info("TURNX AI Director V4 starting...")

# Call startup immediately (Render-safe replacement)
init_app()

# ==========================================================
# MAIN ENTRY (LOCAL RUN ONLY)
# ==========================================================

if __name__ == "__main__":
    port = int(CONFIG.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
