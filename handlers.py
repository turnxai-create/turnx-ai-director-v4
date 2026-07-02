# handlers.py
# TURNX AI Director V4 - Production Handler Layer

from __future__ import annotations

import logging
from typing import Any, Dict

from telegram import telegram, main_menu_keyboard
from director import Director
from premium import premium

logger = logging.getLogger(__name__)


class UpdateHandler:
    """
    Handles all Telegram updates:
    - messages
    - callback queries
    """

    def __init__(self) -> None:
        self.director = Director()

    # ==========================================================
    # ENTRY POINT
    # ==========================================================

    def handle(self, update: Dict[str, Any]) -> None:
        try:
            if "callback_query" in update:
                self._handle_callback(update["callback_query"])
                return

            if "message" in update:
                self._handle_message(update["message"])
                return

        except Exception as e:
            logger.exception(f"Handler error: {e}")

    # ==========================================================
    # MESSAGE HANDLER
    # ==========================================================

    def _handle_message(self, message: Dict[str, Any]) -> None:
        chat_id = message["chat"]["id"]
        text = (message.get("text") or "").strip()

        premium_error = premium.require_access(chat_id)
        if premium_error:
            telegram.send_message(chat_id, premium_error)
            return

        # /start command
        if text == "/start":
            telegram.send_message(
                chat_id,
                "🎬 Welcome to TURNX AI Director V4\nChoose a mode:",
                reply_markup=main_menu_keyboard(),
            )
            return

        # default: treat as creative prompt
        premium.increment_usage(chat_id)

        response = self.director.generate(
            mode="images",
            model="nano_banana_pro_2",
            prompt=text,
            chat_id=chat_id,
        )

        telegram.send_message(chat_id, response)

    # ==========================================================
    # CALLBACK HANDLER
    # ==========================================================

    def _handle_callback(self, callback: Dict[str, Any]) -> None:
        query_id = callback["id"]
        data = callback.get("data", "")
        message = callback["message"]
        chat_id = message["chat"]["id"]

        telegram.answer_callback(query_id)

        premium_error = premium.require_access(chat_id)
        if premium_error:
            telegram.send_message(chat_id, premium_error)
            return

        premium.increment_usage(chat_id)

        # MENU NAVIGATION
        if data == "menu":
            telegram.send_message(
                chat_id,
                "🎬 Main Menu",
                reply_markup=main_menu_keyboard(),
            )
            return

        # MODE SELECTION
        if data.startswith("mode_"):
            mode = data.replace("mode_", "")

            if mode == "images":
                from telegram import image_models_keyboard

                telegram.send_message(
                    chat_id,
                    "🖼 Choose Image Model:",
                    reply_markup=image_models_keyboard(),
                )
                return

            if mode == "video":
                from telegram import video_models_keyboard

                telegram.send_message(
                    chat_id,
                    "🎬 Choose Video Model:",
                    reply_markup=video_models_keyboard(),
                )
                return

            if mode == "image_to_video":
                from telegram import image_to_video_models_keyboard

                telegram.send_message(
                    chat_id,
                    "🎞 Choose I2V Model:",
                    reply_markup=image_to_video_models_keyboard(),
                )
                return

        # IMAGE MODEL SELECTION
        if data.startswith("image_model:"):
            model = data.split(":")[1]

            prompt = "Create a cinematic AI image from user concept"

            result = self.director.generate(
                mode="images",
                model=model,
                prompt=prompt,
                chat_id=chat_id,
            )

            telegram.send_message(chat_id, result)
            return

        # VIDEO MODEL SELECTION
        if data.startswith("video_model:"):
            model = data.split(":")[1]

            prompt = "Create a cinematic AI video from user concept"

            result = self.director.generate(
                mode="video",
                model=model,
                prompt=prompt,
                chat_id=chat_id,
            )

            telegram.send_message(chat_id, result)
            return

        # IMAGE TO VIDEO MODEL SELECTION
        if data.startswith("i2v_model:"):
            model = data.split(":")[1]

            prompt = "Convert image concept into cinematic motion video"

            result = self.director.generate(
                mode="image_to_video",
                model=model,
                prompt=prompt,
                chat_id=chat_id,
            )

            telegram.send_message(chat_id, result)
            return
