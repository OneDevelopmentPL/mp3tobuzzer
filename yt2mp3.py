# github.com/OneDevelopmentPL
import argparse
import yt_dlp
import sys
import os

parser = argparse.ArgumentParser(description="Download YouTube audio as MP3")
parser.add_argument("--url", required=True, help="YouTube video URL")

args = parser.parse_args()

print("[INFO] Starting YouTube audio download...")
print(f"[INFO] URL: {args.url}")

ydl_opts = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "outtmpl": "%(title)s.%(ext)s",
    "remote_components": ["ejs:github"],
    "quiet": False,
    "no_warnings": False,
    "force_ipv4": True,
    "extractor_args": {
        "youtube": {
            "player_client": ["web"]
        }
    },
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.url])
except Exception as e:
    print("[ERROR] Download failed.")
    print(f"[DETAILS] {e}")
    sys.exit(1)

print("[SUCCESS] MP3 download completed successfully.")
