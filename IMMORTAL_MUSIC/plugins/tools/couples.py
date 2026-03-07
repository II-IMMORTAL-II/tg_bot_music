import os
import random
from datetime import datetime, timedelta

from telegraph import upload_file
from PIL import Image, ImageDraw
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from IMMORTAL_MUSIC import app
import config

POLICE = [
    [
        InlineKeyboardButton(
            text="Made by Bolluu",
            url=f"https://t.me/{config.OWNER_USERNAME}",
        ),
    ],
]


def dt():
    now = datetime.now()
    return now.strftime("%d/%m/%Y")


def dt_tom():
    return (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")


tomorrow = dt_tom()
today = dt()


@app.on_message(filters.command("couples"))
async def ctest(_, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("This command only works in groups.")
    try:
        msg = await message.reply_text("Generating couples image...")

        list_of_users = []
        async for i in app.get_chat_members(message.chat.id, limit=50):
            if not i.user.is_bot:
                list_of_users.append(i.user.id)

        if len(list_of_users) < 2:
            await msg.edit_text("Need at least 2 non-bot users in this group.")
            return

        c1_id = random.choice(list_of_users)
        c2_id = random.choice(list_of_users)
        while c1_id == c2_id:
            c2_id = random.choice(list_of_users)

        photo1 = (await app.get_chat(c1_id)).photo
        photo2 = (await app.get_chat(c2_id)).photo

        n1 = (await app.get_users(c1_id)).mention
        n2 = (await app.get_users(c2_id)).mention

        p1_file = f"pfp_{cid}_1.png"
        p2_file = f"pfp_{cid}_2.png"
        out_file = f"test_{cid}.png"

        try:
            p1 = await app.download_media(photo1.big_file_id, file_name=p1_file)
        except Exception:
            p1 = "IMMORTAL_MUSIC/assets/upic.png"
        try:
            p2 = await app.download_media(photo2.big_file_id, file_name=p2_file)
        except Exception:
            p2 = "IMMORTAL_MUSIC/assets/upic.png"

        img1 = Image.open(p1)
        img2 = Image.open(p2)
        img = Image.open("IMMORTAL_MUSIC/assets/cppic.png")

        img1 = img1.resize((437, 437))
        img2 = img2.resize((437, 437))

        mask = Image.new("L", img1.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img1.size, fill=255)

        mask1 = Image.new("L", img2.size, 0)
        draw = ImageDraw.Draw(mask1)
        draw.ellipse((0, 0) + img2.size, fill=255)

        img1.putalpha(mask)
        img2.putalpha(mask1)

        img.paste(img1, (116, 160), img1)
        img.paste(img2, (789, 160), img2)
        img.save(out_file)

        txt = (
            "**Today's Couple of the Day:**\n\n"
            f"{n1} + {n2} = ??\n\n"
            f"**Next couples will be selected on {tomorrow}!**"
        )

        await message.reply_photo(
            out_file,
            caption=txt,
            reply_markup=InlineKeyboardMarkup(POLICE),
        )
        await msg.delete()

        try:
            for x in upload_file(out_file):
                img_url = "https://graph.org/" + x
                _ = {"c1_id": c1_id, "c2_id": c2_id, "img": img_url}
        except Exception:
            pass

    except Exception as e:
        print(str(e))
    finally:
        for f in [f"./downloads/pfp_{cid}_1.png", f"./downloads/pfp_{cid}_2.png", f"test_{cid}.png"]:
            try:
                os.remove(f)
            except Exception:
                pass


__mod__ = "Couples"
__help__ = """
/couples - Generate today's random couple from group members.
"""
