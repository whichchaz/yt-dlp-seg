import argparse
import logging
import os

from pathlib import Path
import subprocess
import yt_dlp

logger = logging.getLogger()


def get_info(link):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
    return info["title"], info["id"]


def download(working_dir, yid):
    if not Path(f"{working_dir}/{yid}.mp4").is_file():
        cmd = [
            "yt-dlp",
            yid,
            "-f",
            "18",
            "-o",
            f"{working_dir}/{yid}.mp4",
        ]
        logger.info(" ".join(cmd))
        subprocess.call(cmd)


def segments(working_dir, yid):
    if not Path(f"{working_dir}/{yid}.mp4").is_file():
        return

    cmd = [
        "ffmpeg",
        "-i",
        f"{working_dir}/{yid}.mp4",
        "-map",
        "0",
        "-b:a",
        "48k",
        "-b:v",
        "300k",
        "-f",
        "scale='432:-2'",
        "-f",
        "segment",
        "-segment_time",
        "1800",
        "-reset_timestamps",
        "1",
        f"{working_dir}/{yid}-%01d.mp4",
    ]
    logger.info(" ".join(cmd))
    subprocess.call(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("link")

    args = parser.parse_args()
    title, id = get_info(args.link)

    path = os.path.join("./downloads", id)
    if not os.path.exists(path):
        os.makedirs(path)
    download(path, id)
    segments(path, id)
