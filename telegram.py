telegram.py

Part 1

from future import annotations

import json
import logging
from typing import Any

from flask import Blueprint, Response, request

from handlers import UpdateHandler

logger = logging.getLogger(name)

telegram_bp = Blueprint("telegram", name)

class TelegramWebhook:
"""
Telegram webhook entry point.

Responsibilities:  
- Receive Telegram webhook updates.  
- Validate JSON.  
- Forward updates to UpdateHandler.  
- Never contain business logic.  
"""  

def __init__(self) -> None:  
    self.handler = UpdateHandler()  

def process(self, payload: dict[str, Any]) -> None:  
    try:  
        self.handler.handle(payload)  
    except Exception:  
        logger.exception("Failed to process Telegram update.")

webhook = TelegramWebhook()

@telegram_bp.route("/webhook", methods=["POST"])
def telegram_webhook() -> Response:
if not request.is_json:
return Response(status=400)

try:  
    payload = request.get_json(force=True)  
except Exception:  
    logger.exception("Invalid Telegram payload.")  
    return Response(status=400)  

webhook.process(payload)  

return Response(  
    response=json.dumps({"ok": True}),  
    status=200,  
    mimetype="application/json",  
)

@telegram_bp.route("/", methods=["GET"])
def healthcheck() -> Response:
return Response(
response=json.dumps(
{
"service": "TURNX AI Director V4",
"status": "running",
}
),
status=200,
mimetype="application/json",
)

def register(app) -> None:
"""
Register Telegram routes into Flask app.
"""
app.register_blueprint(telegram_bp)

telegram.py

Part 2

from future import annotations

import logging
from typing import Any

import requests

from config import BOT_TOKEN

logger = logging.getLogger(name)

class TelegramAPI:
"""
Telegram Bot API client.

This class contains only Telegram API communication.  
Business logic belongs in handlers.py.  
"""  

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"  

def __init__(self, timeout: int = 30) -> None:  
    self.timeout = timeout  

def _request(  
    self,  
    method: str,  
    payload: dict[str, Any],  
) -> dict[str, Any]:  

    response = requests.post(  
        f"{self.BASE_URL}/{method}",  
        json=payload,  
        timeout=self.timeout,  
    )  

    response.raise_for_status()  

    data = response.json()  

    if not data.get("ok"):  
        raise RuntimeError(  
            f"Telegram API error: {data}"  
        )  

    return data  

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

    if reply_markup is not None:  
        payload["reply_markup"] = reply_markup  

    return self._request(  
        "sendMessage",  
        payload,  
    )  

def edit_message(  
    self,  
    chat_id: int,  
    message_id: int,  
    text: str,  
    parse_mode: str = "Markdown",  
    reply_markup: dict[str, Any] | None = None,  
) -> dict[str, Any]:  

    payload: dict[str, Any] = {  
        "chat_id": chat_id,  
        "message_id": message_id,  
        "text": text,  
        "parse_mode": parse_mode,  
    }  

    if reply_markup is not None:  
        payload["reply_markup"] = reply_markup  

    return self._request(  
        "editMessageText",  
        payload,  
    )  

def answer_callback(  
    self,  
    callback_query_id: str,  
    text: str = "",  
    show_alert: bool = False,  
) -> dict[str, Any]:  

    return self._request(  
        "answerCallbackQuery",  
        {  
            "callback_query_id": callback_query_id,  
            "text": text,  
            "show_alert": show_alert,  
        },  
    )  

def delete_message(  
    self,  
    chat_id: int,  
    message_id: int,  
) -> dict[str, Any]:  

    return self._request(  
        "deleteMessage",  
        {  
            "chat_id": chat_id,  
            "message_id": message_id,  
        },  
    )  

def send_chat_action(  
    self,  
    chat_id: int,  
    action: str = "typing",  
) -> dict[str, Any]:  

    return self._request(  
        "sendChatAction",  
        {  
            "chat_id": chat_id,  
            "action": action,  
        },  
    )

telegram = TelegramAPI()

telegram.py

Part 3 (Final)

from future import annotations

from typing import Any

def inline_keyboard(rows: list[list[tuple[str, str]]]) -> dict[str, Any]:
"""
Build a Telegram inline keyboard.

Example:  
inline_keyboard([  
    [("Images", "mode_images")],  
    [("Video", "mode_video")],  
])  
"""  

keyboard: list[list[dict[str, str]]] = []  

for row in rows:  
    keyboard.append(  
        [  
            {  
                "text": text,  
                "callback_data": callback_data,  
            }  
            for text, callback_data in row  
        ]  
    )  

return {  
    "inline_keyboard": keyboard,  
}

def remove_keyboard() -> dict[str, Any]:
"""
Remove the current inline keyboard.
"""

return {  
    "inline_keyboard": [],  
}

def main_menu_keyboard() -> dict[str, Any]:
"""
TURNX AI Director V4 root generation menu.
Only the three supported generation modes are exposed.
"""

return inline_keyboard(  
    [  
        [("🖼 Images", "mode_images")],  
        [("🎬 Video", "mode_video")],  
        [("🎞 Image → Video", "mode_image_to_video")],  
    ]  
)

def image_models_keyboard() -> dict[str, Any]:
"""
Supported image generation models.
"""

return inline_keyboard(  
    [  
        [("Nano Banana Pro 2", "image_model:nano_banana_pro_2")],  
        [("Nano Banana Pro", "image_model:nano_banana_pro")],  
        [("ChatGPT Image 2.0", "image_model:chatgpt_image_2")],  
        [("⬅ Back", "menu")],  
    ]  
)

def video_models_keyboard() -> dict[str, Any]:
"""
Supported video generation models.
"""

return inline_keyboard(  
    [  
        [("Veo 3.1", "video_model:veo_3_1")],  
        [("Omni", "video_model:omni")],  
        [("Seedance", "video_model:seedance")],  
        [("Grok", "video_model:grok")],  
        [("⬅ Back", "menu")],  
    ]  
)

def image_to_video_models_keyboard() -> dict[str, Any]:
"""
Supported Image → Video models.
"""

return inline_keyboard(  
    [  
        [("Veo 3.1", "i2v_model:veo_3_1")],  
        [("Omni", "i2v_model:omni")],  
        [("Seedance", "i2v_model:seedance")],  
        [("Grok", "i2v_model:grok")],  
        [("⬅ Back", "menu")],  
    ]  
)
