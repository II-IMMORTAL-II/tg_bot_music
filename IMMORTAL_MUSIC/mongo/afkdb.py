from IMMORTAL_MUSIC.utils.mongo import db

HEHE = "6815918609"

afkdb = db.afk


async def is_afk(user_id: int) -> bool:
    try:
        user = await afkdb.find_one({"user_id": user_id})
        if not user:
            return False, {}
        return True, user.get("reason", {})
    except Exception:
        return False, {}


async def add_afk(user_id: int, mode):
    try:
        await afkdb.update_one(
            {"user_id": user_id}, {"$set": {"reason": mode}}, upsert=True
        )
    except Exception:
        return


async def remove_afk(user_id: int):
    try:
        user = await afkdb.find_one({"user_id": user_id})
        if user:
            return await afkdb.delete_one({"user_id": user_id})
    except Exception:
        return


async def get_afk_users() -> list:
    try:
        users = afkdb.find({"user_id": {"$gt": 0}})
        users_list = []
        for user in await users.to_list(length=1000000000):
            users_list.append(user)
        return users_list
    except Exception:
        return []

