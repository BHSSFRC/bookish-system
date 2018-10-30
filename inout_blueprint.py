from camera_opencv import Camera
import cv_processing
from disc import d as discerd
from flask import Blueprint, render_template, redirect

in_page = Blueprint("in_page", __name__, template_folder="templates")


@in_page.route("/confirm_user")
def discord_test():
    barcodes = cv_processing.scan_barcodes(Camera().get_frame()[1])
    if barcodes is not None and len(barcodes) >= 1:
        d_id = barcodes[0].data.decode("utf-8")
        user = discerd.get_guild_member(286174293006745601, d_id)
        r = [discerd.get_guild_role(286174293006745601, role) for role in user["roles"]]
        return render_template(
            "discord.html",
            nick=user["nick"],
            username=user["user"]["username"],
            discrim=user["user"]["discriminator"],
            roles=r,
            pfp=discerd.get_pfp_url(d_id),
        )
    else:
        return redirect("/")


def clock_in(user: int):
    """clock in user via d id"""
    pass


def clock_out(user: int):
    """clock out user via d id"""
    pass
