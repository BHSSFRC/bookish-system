import asyncio
import cv_processing
from camera_opencv import Camera
import os
from flask import Flask, render_template, Response, send_from_directory

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def gen(c):
    while True:
        d_frame = cv_processing.draw_debugs_jpegs(c.get_frame()[1])
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + d_frame + b"\r\n")


@app.route("/video_feed")
def feed():
    """Streaming route (img src)"""
    # g = cv_processing.gen_debugs_responses(Camera.frames()[1])
    return Response(gen(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


@app.route("/d_test")
def discord_test():
    d_id = cv_processing.scan_barcodes(Camera().get_frame()[1])[0].data.decode("utf-8")
    return render_template("discord.html", discord_id=d_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
