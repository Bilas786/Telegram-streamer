from flask import Flask, request, Response
from pyrogram import Client
import os

app = Flask(__name__)

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

client = Client("streamer", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.route("/")
def home():
    return "MTProto Telegram Video Streamer Running!"

@app.route("/video")
def stream_video():
    file_id = request.args.get("id")
    if not file_id:
        return "No file ID provided", 400

    def generate():
        with client:
            msg = client.get_messages("-1002734341593", int(file_id))
            for chunk in client.download_media(msg, in_memory=True):
                yield chunk

    return Response(generate(), mimetype="video/mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
