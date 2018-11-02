import cv2
from typing import List
from pyzbar import pyzbar


def scan_barcodes(frame) -> List[pyzbar.Decoded]:
    return pyzbar.decode(frame)


def draw_debugs(frame):
    barcodes = scan_barcodes(frame)
    for bar in barcodes:
        (x, y, w, h) = bar.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (172, 172, 0), 2)
        text = "{} [{}]".format(bar.data.decode("utf-8"), bar.type)
        cv2.putText(
            frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (172, 172, 0), 2
        )
    return frame


def draw_debugs_jpegs(frame):
    debugged = draw_debugs(frame)
    return cv2.imencode(".jpg", debugged)[1].tobytes()
