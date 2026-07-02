"""
telegram.py
TURNX AI Director V4

Telegram Bot API wrapper and Flask webhook routes.
"""

from __future__ import annotations

import logging
from typing import Any

import requests
from flask import Blueprint, Response, jsonify, request

from config import BOT_TOKEN

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Telegram API
# ----------------------------------------------------------------------


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

        if not data.get("ok", False):
            raise RuntimeError(data)

        return data

    # --------------------------------------------------------------

    def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: str = "Markdown",
        disable_web_page_preview: bool = True,
        reply_markup: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
        }

        if reply_markup:
            payload["reply_markup"] = reply_markup

        return self._post("sendMessage", payload)

    # --------------------------------------------------------------

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

        if reply_markup:
            payload["reply_markup"] = reply_markup

        return self._post("editMessageText", payload)

    # --------------------------------------------------------------

    def answer_callback(
        self,
        callback_query_id: str,
        text: str = "",
        show_alert: bool = False,
    ) -> dict[str, Any]:

        return self._post(
            "answerCallbackQuery",
            {
                "callback_query_id": callback_query_id,
                "text": text,
                "show_alert": show_alert,
            },
        )

    # --------------------------------------------------------------

    def delete_message(
        self,
        chat_id: int,
        message_id: int,
    ) -> dict[str, Any]:

        return self._post(
            "deleteMessage",
            {
                "chat_id": chat_id,
                "message_id": message_id,
            },
        )

    # --------------------------------------------------------------

    def send_chat_action(
        self,
        chat_id: int,
        action: str = "typing",
    ) -> dict[str, Any]:

        return self._post(
            "sendChatAction",
            {
                "chat_id": chat_id,
                "action": action,
            },
        )


telegram = TelegramAPI()

# ----------------------------------------------------------------------
# Keyboards
# ----------------------------------------------------------------------


def inline_keyboard(
    rows: list[list[tuple[str, str]]],
) -> dict[str, Any]:

    return {
        "inline_keyboard": [
            [
                {
                    "text": text,
                    "callback_data": callback,
                }
                for text, callback in row
            ]
            for row in rows
        ]
    }


def main_menu_keyboard():

    return inline_keyboard(
        [
            [("🖼 Images", "mode_images")],
            [("🎬 Video", "mode_video")],
            [("🎞 Image → Video", "mode_image_to_video")],
        ]
    )


def image_models_keyboard():

    return inline_keyboard(
        [
            [("Nano Banana Pro 2", "image_model:nano_banana_pro_2")],
            [("Nano Banana Pro", "image_model:nano_banana_pro")],
            [("ChatGPT Image 2.0", "image_model:chatgpt_image_2")],
            [("⬅ Back", "menu")],
        ]
    )


def video_models_keyboard():

    return inline_keyboard(
        [
            [("Veo 3.1", "video_model:veo_3_1")],
            [("Omni", "video_model:omni")],
            [("Seedance", "video_model:seedance")],
            [("Grok", "video_model:grok")],
            [("⬅ Back", "menu")],
        ]
    )


def image_to_video_models_keyboard():

    return inline_keyboard(
        [
            [("Veo 3.1", "i2v_model:veo_3_1")],
            [("Omni", "i2v_model:omni")],
            [("Seedance", "i2v_model:seedance")],
            [("Grok", "i2v_model:grok")],
            [("⬅ Back", "menu")],
        ]
    }


# ----------------------------------------------------------------------
# Flask Blueprint
# ----------------------------------------------------------------------

telegram_bp = Blueprint("telegram", __name__)


@telegram_bp.route("/", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "running",
            "service": "TURNX AI Director V4",
        }
    )


@telegram_bp.route("/webhook", methods=["POST"])
def webhook() -> Response:

    if not request.is_json:
        return Response(status=400)

    update = request.get_json(silent=True)

    if update is None:
        return Response(status=400)

    try:
        # Lazy import prevents circular imports.
        from handlers import UpdateHandler

        UpdateHandler().handle(update)

    except Exception:
        logger.exception("Telegram update failed.")
        return Response(status=500)

    return jsonify({"ok": True})


def register(app) -> None:
    app.register_blueprint(telegram_bp)
