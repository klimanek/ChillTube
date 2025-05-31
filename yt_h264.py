#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import shutil
import time
import logging
import platform
from pathlib import Path

# Add /usr/local/bin do PATH if not already present
path = os.environ.get("PATH", "")
if "/usr/local/bin" not in path:
    os.environ["PATH"] = f"{path}:/usr/local/bin"

# Logger
LOGFILE_PATH = Path.home()/"yt_h264.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logfile = logging.FileHandler(LOGFILE_PATH)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logfile.setFormatter(formatter)

logger.addHandler(logfile)

# Functions
def read_message():
    try:
        # Give it a moment
        time.sleep(0.1)

        # Read 4 bytes representing message length
        raw_length = sys.stdin.buffer.read(4)

        logger.info(f"read_message - Raw length bytes: {raw_length}")

        if len(raw_length) == 0:
            logger.info("Native host received no message length, exiting gracefully.")
            sys.exit(0)

        message_length = int.from_bytes(raw_length, byteorder='little')
        logger.info(f"read_message - Message length: {message_length}")

        # Read the msg
        message_bytes = sys.stdin.buffer.read(message_length)
        logger.info(f"read_message - Message bytes: {message_bytes}")

        if len(message_bytes) < message_length:
            logger.error(f"read_message - Expected {message_length} bytes, got {len(message_bytes)}.")
            sys.exit(1)

        message = message_bytes.decode('utf-8')
        logger.info(f"read_message - Decoded message: {message}")
        return json.loads(message)

    except json.JSONDecodeError as e:
        logger.error(f"read_message - Invalid JSON received: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"read_message - An unexpected error occurred: {e}")
        sys.exit(1)

def send_message(message):
    encoded = json.dumps(message).encode('utf-8')
    sys.stdout.buffer.write(len(encoded).to_bytes(4, byteorder='little'))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()

def extract_h264_urls(url):
    """Returns a tuple (video_url, audio_url) or (None, None) if extraction fails."""
    try:
        result = subprocess.run(
            ["yt-dlp",
             "-f", "bv*[vcodec^=avc1][height<=1080]+ba[acodec^=mp4a]",
             "--get-url",
             url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        streams = result.stdout.strip().splitlines()

        if len(streams) == 2:
            return streams[0], streams[1]  # video_url, audio_url
        else:
            logger.info(f"extract_h264_urls - yt-dlp output: {result.stdout.strip()}")
            return None, None

    except Exception as e:
        logger.error(f"extract_h264_urls - An error occurred: {e}")
        return None, None


def handle_message(received):
    url = received.get('text')

    if platform.system() in {"Darwin", "Windows"}:
        logger.warning("Unsupported platform: %s", platform.system())
        send_message({"status": "Error", "reason": "Unsupported OS"})
        return

    if not url:
        logger.error("handle_message - No URL received.")
        send_message({"status": "Error", "reason": "No URL received"})
        return

    player = None
    player_name = "mpv"

    if shutil.which(player_name):
        player = [
            player_name,
            "--ytdl-format=bv*[vcodec^=avc1][height<=1080]+ba[acodec^=mp4a]/b[vcodec^=avc1][height<=1080]",
            url
        ]
        logger.info(f"handle_message - MPV found. Command: {player}")
    else:
        logger.error("handle_message - MPV not found.")
        send_message({"status": "Error", "reason": "MPV not found"})
        return

    try:
        subprocess.Popen(player)
        logger.info("handle_message - MPV launched successfully.")
        send_message({"status": "Success"})
    except Exception as e:
        logger.error(f"handle_message - Failed to launch MPV: {e}")
        send_message({"status": "Error", "reason": f"MPV launch failed: {str(e)}"})


# Main
def main():
    logger.info("main - Native messaging host started.")

    while True:
        try:
            received = read_message()
            handle_message(received)
        except Exception as e:
            logger.error(f"main - Unexpected error: {e}")
            send_message({"status": "Error", "reason": f"Unexpected error: {str(e)}"})


if __name__ == '__main__':
    main()
