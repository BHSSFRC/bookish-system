from . import cv_processing
from .camera_opencv import Camera
import os
from flask import Flask, redirect, render_template, Response, send_from_directory
from .disc import d as discerd
from .blueprints.clocker.inout_blueprint import in_page

app = Flask(__name__.split(".")[0])
app.register_blueprint(in_page, url_prefix="/tick_tock")


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
    return Response(gen(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


@app.template_filter()
def int_to_hexcolor(i) -> str:
    return "#" + (hex(i)[2:] if i != 0 else "FFFFFF")
