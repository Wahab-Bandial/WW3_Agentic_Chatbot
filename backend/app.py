from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_response
import logging
from dotenv import load_dotenv

# Load GROQ_API_KEY from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def home():
    return "WW3 ChatBot Flask server is running fast!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    logging.debug(f"Incoming message: {user_message}")

    if not user_message or not user_message.strip():
        return jsonify({"reply": "No message provided."})

    try:
        reply = get_response(user_message)
        logging.debug(f"Bot reply: {reply}")
        return jsonify({"reply": reply})
    except Exception as e:
        logging.error(f"Error generating response: {e}", exc_info=True)
        return jsonify({"reply": "Error processing your message."})

# ✅ This keeps Flask running
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False, use_reloader=False)

