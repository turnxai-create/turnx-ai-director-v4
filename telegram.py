# telegram.py
# TURNX AI Director V4 - FIXED CLEAN VERSION

from __future__ import annotations

import logging
from typing import Any

import requests
from flask import Blueprint, Response, jsonify, request

from config import BOT_TOKEN

logger = logging.getLogger(__name__)

# ==========================================================
# Telegram API WRAPPER
# ==========================================================

class TelegramAPI:
    BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def _post(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(
            f"{self.BASE_URL}/{method}",
            json=payload,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("ok"):
            raise RuntimeError(data)

        return data

    def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: str = "Markdown",
        reply_markup: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }

        if reply_markup is not None:
            payload["reply_markup"] = reply_markup

        return self._post("sendMessage", payload)

    def edit_message(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: str = "Markdown",
        reply_markup: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode,
        }

        if reply_markup is not None:
            payload["reply_markup"] = reply_markup

        return self._post("editMessageText", payload)

    def answer_callback(
        self,
        callback_query_id: str,
        text: str = "",
    ) -> dict[str, Any]:

        return self._post(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_query_id,
                "text": text,
            },
        )

    def send_chat_action(self, chat_id: int, action: str = "typing") -> dict[str, Any]:
        return self._post(
            "sendChatAction",
            {
                "chat_id": chat_id,
                "action": action,
            },
        )


telegram = TelegramAPI()

# ==========================================================
# KEYBOARDS
# ==========================================================

def main_menu_keyboard() -> dict[str, Any]:
    return {
        "inline_keyboard": [
            [{"text": "🖼 Images", "callback_data": "mode_images"}],
            [{"text": "🎬 Video", "callback_data": "mode_video"}],
            [{"text": "🎞 Image → Video", "callback_data": "mode_image_to_video"}],
        ]
    }


def image_models_keyboard() -> dict[str, Any]:
    return {
        "inline_keyboard": [
            [{"text": "Nano Banana Pro 2", "callback_data": "image_model:nano_banana_pro_2"}],
            [{"text": "Nano Banana Pro", "callback_data": "image_model:nano_banana_pro"}],
            [{"text": "ChatGPT Image 2.0", "callback_data": "image_model:chatgpt_image_2"}],
            [{"text": "⬅ Back", "callback_data": "menu"}],
        ]
    }


def video_models_keyboard() -> dict[str, Any]:
    return {
        "inline_keyboard": [
            [{"text": "Veo 3.1", "callback_data": "video_model:veo_3_1"}],
            [{"text": "Omni", "callback_data": "video_model:omni"}],
            [{"text": "Seedance", "callback_data": "video_model:seedance"}],
            [{"text": "Grok", "callback_data": "video_model:grok"}],
            [{"text": "⬅ Back", "callback_data": "menu"}],
        ]
    }


def image_to_video_models_keyboard() -> dict[str, Any]:
    return {
        "inline_keyboard": [
            [{"text": "Veo 3.1", "callback_data": "i2v_model:veo_3_1"}],
            [{"text": "Omni", "callback_data": "i2v_model:omni"}],
            [{"text": "Seedance", "callback_data": "i2v_model:seedance"}],
            [{"text": "Grok", "callback_data": "i2v_model:grok"}],
            [{"text": "⬅ Back", "callback_data": "menu"}],
        ]
    }

# ==========================================================
# FLASK WEBHOOK
# ==========================================================

telegram_bp = Blueprint("telegram", __name__)


@telegram_bp.route("/webhook", methods=["POST"])
def webhook() -> Response:
    if not request.is_json:
        return Response(status=400)

    update = request.get_json(silent=True)

    if not update:
        return Response(status=400)

    try:
        from handlers import UpdateHandler
        UpdateHandler().handle(update)

    except Exception:
        logger.exception("Webhook error")
        return Response(status=500)

    return jsonify({"ok": True})


@telegram_bp.route("/", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "service": "TURNX AI Director V4",
        }
    )


def register(app) -> None:
    app.register_blueprint(telegram_bp)
