from bookish_system.camera_opencv import Camera
from bookish_system import cv_processing
from datetime import timedelta
from bookish_system.disc import d as discerd
from bookish_system.disc import config
from flask import Blueprint, render_template, redirect
import psycopg2
import time

in_page = Blueprint(
    "in_page", __name__, template_folder="templates", static_folder="static"
)
db_connection = psycopg2.connect(**config.postgresql)

# utility functions
def get_total_time(user: int) -> float:
    cur = db_connection.cursor()
    cur.execute("""SELECT * FROM timetable WHERE member = %s""", (user,))
    ret = cur.fetchone()
    cur.close()
    if ret is not None:
        return ret[1]
    else:
        return 0


def save_clock(clock: dict):
    cur = db_connection.cursor()
    cur.execute("""TRUNCATE timekeeper""")
    for key, value in clock.items():
        cur.execute(
            """INSERT INTO timekeeper (member, time_in) VALUES (%(mem)s, %(timein)s) ON CONFLICT (member) DO UPDATE SET time_in = %(timein)s""",
            {"mem": key, "timein": value},
        )
    db_connection.commit()
    cur.close()


def retrieve_clock() -> dict:
    c = {}
    cur = db_connection.cursor()
    cur.execute("""SELECT * FROM timekeeper""")
    for record in cur:
        c[record[0]] = record[1]
    cur.close()
    return c


@in_page.route("/return_home")
@in_page.route("/")
def return_home():
    return redirect("/")


@in_page.route("/confirm_user")
def discord_test():
    barcodes = cv_processing.scan_barcodes(Camera().get_frame()[1])
    if barcodes is not None and len(barcodes) >= 1:
        d_id = int(barcodes[0].data.decode("utf-8"))
        user_ = discerd.get_guild_member(config.GUILD_ID, d_id)
        r = [discerd.get_guild_role(config.GUILD_ID, role) for role in user_["roles"]]
        total_hours = (
            get_total_time(d_id) / 3600 if get_total_time(d_id) is not None else 0
        )
        return render_template(
            "discord.html",
            user=user_,
            roles=r,
            pfp=discerd.get_pfp_url(d_id),
            recorded_hours=round(total_hours, 2),
            currently_in=d_id in retrieve_clock().keys(),
        )
    else:
        return redirect("/")


@in_page.route("/clock/<int:user>")
def clock(user: int):
    clock_state = retrieve_clock()
    if user in clock_state.keys():
        # clocking out
        total = timedelta(seconds=time.time() - clock_state[user])
        del clock_state[user]
        cur = db_connection.cursor()
        cur.execute(
            """INSERT INTO timetable (member, seconds) VALUES (%(mem)s, %(time)s) ON CONFLICT (member) DO UPDATE SET seconds = timetable.seconds + %(time)s""",
            {"mem": user, "time": total.total_seconds()},
        )
        db_connection.commit()
        cur.close()
        save_clock(clock_state)
        return render_template(
            "in_and_out.html",
            direction="out",
            deltah=round(total.total_seconds() / 3600.0, 2),
        )
    else:
        # clocking in
        clock_state[user] = time.time()
        save_clock(clock_state)
        return render_template("in_and_out.html", direction="in")
