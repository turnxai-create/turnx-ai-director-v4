from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("turnx")


@app.route("/", methods=["GET"])
def home():
    return "TURNX AI Director V4 LIVE", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json(force=True)
        logger.info(f"Update received: {update}")

        from handlers import UpdateHandler

        handler = UpdateHandler()
        handler.process(update)

        return jsonify({"ok": True}), 200

    except Exception as e:
        logger.error("Webhook error", exc_info=True)
        return jsonify({"ok": False}), 200


def register(app_instance):
    passister_blueprint(telegram_bp)
