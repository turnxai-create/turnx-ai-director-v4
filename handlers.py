# handlers.py
# TURNX AI Director V4 - STABLE MODE (NO DIRECTOR LAYER)

from __future__ import annotations

import logging
from typing import Any, Dict

from telegram import telegram, main_menu_keyboard
from premium import premium

from ai import (
    generate_image_prompt,
    generate_video_prompt,
    generate_i2v_prompt,
)

logger = logging.getLogger(__name__)


class UpdateHandler:
    """
    Stable production handler:
    - Direct AI calls (NO director layer)
    - Guaranteed Telegram response
    """

    def handle(self, update: Dict[str, Any]) -> None:
        try:
            if "callback_query" in update:
                self._callback(update["callback_query"])
                return

            if "message" in update:
                self._message(update["message"])
                return

        except Exception as e:
            logger.exception(f"Handler crash prevented: {e}")

    # ==========================================================
    # MESSAGE
    # ==========================================================

    def _message(self, message: Dict[str, Any]) -> None:
        chat_id = message["chat"]["id"]
        text = (message.get("text") or "").strip()

        telegram.send_message(chat_id, "⚙️ Processing...")

        # /start
        if text == "/start":
            telegram.send_message(
                chat_id,
                "🎬 TURNX AI Director V4\nChoose a mode:",
                reply_markup=main_menu_keyboard(),
            )
            return

        # premium check
        err = premium.require_access(chat_id)
        if err:
            telegram.send_message(chat_id, err)
            return

        premium.increment_usage(chat_id)

        # DEFAULT: IMAGE MODE (SAFE FALLBACK)
        result = generate_image_prompt(
            model="nano_banana_pro_2",
            prompt=text,
        )

        telegram.send_message(chat_id, result)

    # ==========================================================
    # CALLBACK
    # ==========================================================

    def _callback(self, callback: Dict[str, Any]) -> None:
        query_id = callback["id"]
        data = callback.get("data", "")
        message = callback["message"]
        chat_id = message["chat"]["id"]

        telegram.answer_callback(query_id)

        err = premium.require_access(chat_id)
        if err:
            telegram.send_message(chat_id, err)
            return

        premium.increment_usage(chat_id)

        # MAIN MENU
        if data == "menu":
            telegram.send_message(
                chat_id,
                "🎬 Main Menu",
                reply_markup=main_menu_keyboard(),
            )
            return

        # MODE SELECTION
        if data == "mode_images":
            telegram.send_message(chat_id, "🖼 Send your image prompt")
            return

        if data == "mode_video":
            telegram.send_message(chat_id, "🎬 Send your video prompt")
            return

        if data == "mode_image_to_video":
            telegram.send_message(chat_id, "🎞 Send your I2V prompt")
            return

        # IMAGE MODEL (simple direct call)
        if data.startswith("image_model:"):
            model = data.split(":")[1]

            result = generate_image_prompt(model=model, prompt="cinematic scene")
            telegram.send_message(chat_id, result)
            return

        # VIDEO MODEL
        if data.startswith("video_model:"):
            model = data.split(":")[1]

            result = generate_video_prompt(model=model, prompt="cinematic video")
            telegram.send_message(chat_id, result)
            return

        # I2V MODEL
        if data.startswith("i2v_model:"):
            model = data.split(":")[1]

            result = generate_i2v_prompt(model=model, prompt="cinematic motion")
            telegram.send_message(chat_id, result)
            return
