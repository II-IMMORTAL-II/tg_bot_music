import os
import shutil
from re import findall
from bing_image_downloader import downloader
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, Message
from IMMORTAL_MUSIC import app

@app.on_message(filters.command(["img", "image"], prefixes=["/", "!"]))
async def google_img_search(client: Client, message: Message):
    chat_id = message.chat.id
    images_dir = None

    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply("â á´˜Ê€á´á´ Éªá´…á´‡ á´€É´ Éªá´á´€É¢á´‡ Ç«á´œÉªá´‡Ê€Ê á´›á´ sá´‡á´€Ê€á´„Êœ!")

    lim = findall(r"lim=\d+", query)
    try:
        lim = int(lim[0].replace("lim=", ""))
        query = query.replace(f"lim={lim}", "")
    except IndexError:
        lim = 6  # Default limit to 6 images

    download_dir = "downloads"

    try:
        downloader.download(query, limit=lim, output_dir=download_dir, adult_filter_off=True, force_replace=False, timeout=60)
        images_dir = os.path.join(download_dir, query)
        if not os.listdir(images_dir):
            raise Exception("No images were downloaded.")
        lst = [os.path.join(images_dir, img) for img in os.listdir(images_dir)][:lim]  # Ensure we only take the number of images specified by lim
    except Exception as e:
        return await message.reply(f"â á´‡Ê€Ê€á´Ê€ ÉªÉ´ á´…á´á´¡É´ÊŸá´á´€á´…ÉªÉ´É¢ Éªá´á´€É¢á´‡s: {e}")

    msg = await message.reply("â Ò“ÉªÉ´á´…ÉªÉ´É¢ Éªá´á´€É¢á´‡s.....")

    count = 0
    for img in lst:
        count += 1
        await msg.edit(f"â Ò“ÉªÉ´á´… {count} Éªá´á´€É¢á´‡s.....")

    try:
        await app.send_media_group(
            chat_id=chat_id,
            media=[InputMediaPhoto(media=img) for img in lst],
            reply_to_message_id=message.id
        )
    except Exception as e:
        return await message.reply(f"â á´‡Ê€Ê€á´Ê€ ÉªÉ´ sá´‡É´á´…ÉªÉ´É¢ Éªá´á´€É¢á´‡s: {e}")
    finally:
        if images_dir and os.path.isdir(images_dir):
            shutil.rmtree(images_dir, ignore_errors=True)
        await msg.delete()

