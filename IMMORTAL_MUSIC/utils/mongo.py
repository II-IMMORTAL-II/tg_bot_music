from typing import Dict

from IMMORTAL_MUSIC.core.mongo import mongodb as db

coupledb = db.couple
afkdb = db.afk
nightmodedb = db.nightmode
notesdb = db.notes
filtersdb = db.filters


async def _get_lovers(cid: int):
    lovers = await coupledb.find_one({"chat_id": cid})
    return lovers["couple"] if lovers else {}


async def _get_image(cid: int):
    lovers = await coupledb.find_one({"chat_id": cid})
    return lovers["img"] if lovers else {}


async def get_couple(cid: int, date: str):
    lovers = await _get_lovers(cid)
    return lovers[date] if date in lovers else False


async def save_couple(cid: int, date: str, couple: Dict, img: str):
    lovers = await _get_lovers(cid)
    lovers[date] = couple
    await coupledb.update_one(
        {"chat_id": cid},
        {"$set": {"couple": lovers, "img": img}},
        upsert=True,
    )
