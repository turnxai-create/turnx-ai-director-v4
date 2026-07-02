from __future__ import annotations

import logging

from flask import Flask

from telegram import register as register_telegram_routes
from config import CONFIG

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("turnx")


def create_app() -> Flask:
    """
    Flask application factory for TURNX AI Director V4.
    """

    app = Flask(__name__)

    # Basic config
    app.config["JSON_SORT_KEYS"] = False

    # Register Telegram webhook routes
    register_telegram_routes(app)

    return app


app = create_app()


@app.before_first_request
def startup_check():
    logger.info("TURNX AI Director V4 starting up...")


@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "ok",
        "service": "TURNX AI Director V4",
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(CONFIG.get("PORT", 5000)),
        debug=False,
    )
# No additional logic required in app.py for V4 architecture.

# This file is intentionally minimal and acts only as the Flask entry point.

# TURNX AI Director V4 follows modular architecture:
# - telegram.py handles webhook routing
# - handlers.py handles logic
# - director.py handles AI prompt generation
# - ai.py handles Groq API calls
# - states.py manages session state

# Production deployment is handled via Render using:
# gunicorn app:app
