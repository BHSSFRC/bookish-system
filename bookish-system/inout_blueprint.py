from .camera_opencv import Camera
from . import cv_processing
from datetime import timedelta
from .disc import d as discerd
from flask import Blueprint, render_template, redirect
import time

in_page = Blueprint("in_page", __name__, template_folder="templates")
clock_state = {}


@in_page.route("/confirm_user")
def discord_test():
    barcodes = cv_processing.scan_barcodes(Camera().get_frame()[1])
    if barcodes is not None and len(barcodes) >= 1:
        d_id = barcodes[0].data.decode("utf-8")
        user = discerd.get_guild_member(286174293006745601, d_id)
        r = [discerd.get_guild_role(286174293006745601, role) for role in user["roles"]]
        return render_template(
            "discord.html",
            discord_id=d_id,
            nick=user["nick"],
            username=user["user"]["username"],
            discrim=user["user"]["discriminator"],
            roles=r,
            pfp=discerd.get_pfp_url(d_id),
        )
    else:
        return redirect("/")


@in_page.route("/clock/<int:user>")
def clock(user: int):
    if user in clock_state.keys():
        # clocking out
        total = timedelta(seconds=time.time() - clock_state[user])
        del clock_state[user]
        return str(total)
    else:
        # clocking in
        clock_state[user] = time.time()
        return "Clocked in"


@in_page.route("/clockin/<int:user>")
def clock_in(user: int):
    """clock in user via d id"""
    clock_state[user] = time.time()


@in_page.route("/clockout/<int:user>")
def clock_out(user: int):
    """clock out user via d id"""
    time_in = clock_state[user]
    total = timedelta(seconds=time.time() - time_in)