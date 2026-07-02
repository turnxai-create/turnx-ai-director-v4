# handlers.py
# Part 1

from __future__ import annotations

import logging
from typing import Any

from director import Director
from states import UserStateManager
from telegram import (
    telegram,
    main_menu_keyboard,
    image_models_keyboard,
    video_models_keyboard,
    image_to_video_models_keyboard,
)

logger = logging.getLogger(__name__)


class UpdateHandler:
    """
    Main Telegram update dispatcher.

    Responsibilities:
    - Parse Telegram updates.
    - Route messages/callbacks.
    - Delegate prompt generation to Director.
    - Manage user state.
    """

    def __init__(self) -> None:
        self.states = UserStateManager()
        self.director = Director()

    def handle(self, update: dict[str, Any]) -> None:
        if "message" in update:
            self._handle_message(update["message"])
            return

        if "callback_query" in update:
            self._handle_callback(update["callback_query"])
            return

    # ------------------------------------------------------------------ #
    # Message Handling
    # ------------------------------------------------------------------ #

    def _handle_message(self, message: dict[str, Any]) -> None:
        chat_id = message["chat"]["id"]

        text = message.get("text", "").strip()

        if not text:
            telegram.send_message(
                chat_id,
                "Please send a text prompt.",
            )
            return

        if text.startswith("/start"):
            self._start(chat_id)
            return

        if text.startswith("/menu"):
            self._menu(chat_id)
            return

        state = self.states.get(chat_id)

        if state is None:
            telegram.send_message(
                chat_id,
                "Select a generation mode first.",
                reply_markup=main_menu_keyboard(),
            )
            return

        telegram.send_chat_action(chat_id)

        result = self.director.generate(
            mode=state.mode,
            model=state.model,
            prompt=text,
            chat_id=chat_id,
        )

        telegram.send_message(chat_id, result)

    # ------------------------------------------------------------------ #
    # Callback Handling
    # ------------------------------------------------------------------ #

    def _handle_callback(self, callback: dict[str, Any]) -> None:
        data = callback["data"]

        chat_id = callback["message"]["chat"]["id"]
        message_id = callback["message"]["message_id"]

        telegram.answer_callback(callback["id"])

        if data == "menu":
            telegram.edit_message(
                chat_id,
                message_id,
                "Choose a generation mode.",
                reply_markup=main_menu_keyboard(),
            )
            return

        if data == "mode_images":
            telegram.edit_message(
                chat_id,
                message_id,
                "Choose an image model.",
                reply_markup=image_models_keyboard(),
            )
            return

        if data == "mode_video":
            telegram.edit_message(
                chat_id,
                message_id,
                "Choose a video model.",
                reply_markup=video_models_keyboard(),
            )
            return

        if data == "mode_image_to_video":
            telegram.edit_message(
                chat_id,
                message_id,
                "Choose an Image → Video model.",
                reply_markup=image_to_video_models_keyboard(),
            )
            return

        if data.startswith("image_model:"):
            self._select_model(
                chat_id,
                message_id,
                "images",
                data.split(":", 1)[1],
            )
            return

        if data.startswith("video_model:"):
            self._select_model(
                chat_id,
                message_id,
                "video",
                data.split(":", 1)[1],
            )
            return

        if data.startswith("i2v_model:"):
            self._select_model(
                chat_id,
                message_id,
                "image_to_video",
                data.split(":", 1)[1],
            )

    # ------------------------------------------------------------------ #
    # Commands
    # ------------------------------------------------------------------ #

    def _start(self, chat_id: int) -> None:
        self.states.clear(chat_id)

        telegram.send_message(
            chat_id,
            (
                "🎬 *TURNX AI Director V4*\n\n"
                "Award-winning AI Creative Director.\n\n"
                "Choose a generation mode."
            ),
            reply_markup=main_menu_keyboard(),
        )

    def _menu(self, chat_id: int) -> None:
        telegram.send_message(
            chat_id,
            "Choose a generation mode.",
            reply_markup=main_menu_keyboard(),
        )

    # ------------------------------------------------------------------ #
    # State
    # ------------------------------------------------------------------ #

    def _select_model(
        self,
        chat_id: int,
        message_id: int,
        mode: str,
        model: str,
    ) -> None:

        self.states.set(
            chat_id=chat_id,
            mode=mode,
            model=model,
        )

        telegram.edit_message(
            chat_id,
            message_id,
            (
                f"✅ *Mode:* `{mode}`\n"
                f"✅ *Model:* `{model}`\n\n"
                "Now send your idea.\n\n"
                "TURNX AI Director will plan first and generate a premium production-ready prompt."
            ),
            )
