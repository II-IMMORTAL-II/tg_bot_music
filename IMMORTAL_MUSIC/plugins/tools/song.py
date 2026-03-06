import os

import requests
import yt_dlp
from pyrogram import filters

from ... import app
from config import SUPPORT_CHAT


def _duration_to_seconds(duration: str) -> int:
    if not duration:
        return 0
    try:
        parts = [int(p) for p in duration.split(":")]
    except ValueError:
        return 0
    total = 0
    for part in parts:
        total = total * 60 + part
    return total


@app.on_message(filters.command(["song", "music"]))
async def song(_, message):
    await message.delete()

    if len(message.command) < 2:
        return await message.reply_text("Usage: /song <song name>")

    query = " ".join(message.command[1:]).strip()
    user = message.from_user
    mention = f"[{user.first_name}](tg://user?id={user.id})" if user else "Unknown"

    status = await message.reply_text("Searching song, please wait...")

    audio_file = None
    thumb_name = None

    try:
        search_opts = {"quiet": True, "no_warnings": True, "noplaylist": True}
        with yt_dlp.YoutubeDL(search_opts) as ydl:
            search = ydl.extract_info(f"ytsearch1:{query}", download=False)

        entries = search.get("entries") if isinstance(search, dict) else None
        if not entries:
            return await status.edit_text("Song not found on YouTube.")

        info = entries[0]
        video_id = info.get("id")
        if not video_id:
            return await status.edit_text("Song not found on YouTube.")

        title = (info.get("title") or query)[:80]
        duration_seconds = int(info.get("duration") or 0)
        duration_text = info.get("duration_string") or "Unknown"
        views = info.get("view_count") or 0

        thumbnail = info.get("thumbnail")
        if thumbnail:
            thumb_name = f"thumb_{video_id}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True, timeout=20)
            thumb.raise_for_status()
            with open(thumb_name, "wb") as f:
                f.write(thumb.content)

        await status.edit_text("Downloading audio, please wait...")

        download_opts = {
            "format": "bestaudio[ext=m4a]/bestaudio",
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "outtmpl": "downloads/%(id)s.%(ext)s",
        }
        video_link = f"https://www.youtube.com/watch?v={video_id}"
        with yt_dlp.YoutubeDL(download_opts) as ydl:
            info_dict = ydl.extract_info(video_link, download=True)
            audio_file = ydl.prepare_filename(info_dict)

        if not duration_seconds:
            duration_seconds = _duration_to_seconds(duration_text)

        caption = (
            f"**Title:** {title}\n"
            f"**Duration:** `{duration_text}`\n"
            f"**Views:** `{views}`\n"
            f"**Requested by:** {mention}"
        )

        await message.reply_audio(
            audio=audio_file,
            caption=caption,
            performer=app.name,
            thumb=thumb_name if thumb_name and os.path.exists(thumb_name) else None,
            title=title,
            duration=duration_seconds,
        )
        await status.delete()
    except Exception as e:
        await status.edit_text(
            f"Download failed. Report in [support chat]({SUPPORT_CHAT}).\nError: `{e}`",
            disable_web_page_preview=True,
        )
    finally:
        for file_path in (audio_file, thumb_name):
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass
