import logging

logger = logging.getLogger("turnx")


class UpdateHandler:
    def __init__(self):
        from ai import (
            generate_image_prompt,
            generate_video_prompt,
            generate_i2v_prompt
        )
        self.generate_image_prompt = generate_image_prompt
        self.generate_video_prompt = generate_video_prompt
        self.generate_i2v_prompt = generate_i2v_prompt

    def process(self, update: dict):
        """
        Main entry point for Telegram updates.
        """

        try:
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")

            if not chat_id or not text:
                return

            logger.info(f"Chat {chat_id}: {text}")

            response = self.route(text)

            self.send_message(chat_id, response)

        except Exception as e:
            logger.error(f"Handler error: {e}", exc_info=True)

    def route(self, text: str) -> str:
        text_lower = text.lower()

        if "image" in text_lower:
            return self.generate_image_prompt("Nano Banana Pro 2", text)

        if "video" in text_lower:
            return self.generate_video_prompt("Veo 3.1", text)

        if "image to video" in text_lower or "i2v" in text_lower:
            return self.generate_i2v_prompt("Seedance", text)

        return self.generate_image_prompt("ChatGPT Image 2.0", text)

    def send_message(self, chat_id: int, text: str):
        """
        Safe fallback sender (no external dependency required)
        """
        import requests
        from config import BOT_TOKEN

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        try:
            requests.post(url, json={
                "chat_id": chat_id,
                "text": text
            })
        except Exception as e:
            logger.error(f"Send message failed: {e}")
