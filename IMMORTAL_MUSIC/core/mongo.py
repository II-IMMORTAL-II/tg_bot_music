from urllib.parse import urlparse

from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient

import config

from ..logger import LOGGER


class _InMemoryCursor:
    def __init__(self, docs):
        self._docs = docs
        self._idx = 0

    def __aiter__(self):
        self._idx = 0
        return self

    async def __anext__(self):
        if self._idx >= len(self._docs):
            raise StopAsyncIteration
        doc = self._docs[self._idx]
        self._idx += 1
        return dict(doc)

    async def to_list(self, length=None):
        if length is None or length < 0:
            return [dict(x) for x in self._docs]
        return [dict(x) for x in self._docs[:length]]


class _InMemoryCollection:
    def __init__(self):
        self._docs = []

    @staticmethod
    def _match_condition(value, condition):
        if not isinstance(condition, dict):
            return value == condition
        for op, expected in condition.items():
            if op == "$gt" and not (value > expected):
                return False
            if op == "$lt" and not (value < expected):
                return False
            if op == "$gte" and not (value >= expected):
                return False
            if op == "$lte" and not (value <= expected):
                return False
            if op == "$ne" and not (value != expected):
                return False
        return True

    @classmethod
    def _match(cls, doc, query):
        if not query:
            return True
        for key, condition in query.items():
            if not cls._match_condition(doc.get(key), condition):
                return False
        return True

    @staticmethod
    def _project(doc, projection):
        if not projection:
            return dict(doc)
        result = {}
        include = [k for k, v in projection.items() if v and k != "_id"]
        if include:
            for key in include:
                if key in doc:
                    result[key] = doc[key]
            return result
        for key, value in doc.items():
            if key not in projection or projection[key]:
                result[key] = value
        return result

    async def find_one(self, query=None, projection=None):
        for doc in self._docs:
            if self._match(doc, query or {}):
                return self._project(doc, projection)
        return None

    def find(self, query=None, projection=None):
        docs = [
            self._project(doc, projection)
            for doc in self._docs
            if self._match(doc, query or {})
        ]
        return _InMemoryCursor(docs)

    async def count_documents(self, query=None):
        return sum(1 for doc in self._docs if self._match(doc, query or {}))

    async def insert_one(self, doc):
        self._docs.append(dict(doc))
        return {"inserted_id": len(self._docs)}

    async def delete_one(self, query):
        for i, doc in enumerate(self._docs):
            if self._match(doc, query):
                self._docs.pop(i)
                return {"deleted_count": 1}
        return {"deleted_count": 0}

    async def update_one(self, query, update, upsert=False):
        target = None
        for doc in self._docs:
            if self._match(doc, query):
                target = doc
                break

        if target is None and upsert:
            target = dict(query)
            self._docs.append(target)

        if target is None:
            return {"matched_count": 0, "modified_count": 0}

        if any(k.startswith("$") for k in update.keys()):
            if "$set" in update:
                target.update(update["$set"])
            if "$push" in update:
                for key, value in update["$push"].items():
                    target.setdefault(key, [])
                    target[key].append(value)
            if "$pull" in update:
                for key, value in update["$pull"].items():
                    existing = target.get(key, [])
                    if isinstance(existing, list):
                        target[key] = [x for x in existing if x != value]
        else:
            target.update(update)
        return {"matched_count": 1, "modified_count": 1}


class _InMemoryDatabase:
    def __init__(self):
        self._collections = {}

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        if name not in self._collections:
            self._collections[name] = _InMemoryCollection()
        return self._collections[name]

    def __getitem__(self, name):
        return self.__getattr__(name)

    async def command(self, name):
        if str(name).lower() == "dbstats":
            collections = len(self._collections)
            objects = sum(len(col._docs) for col in self._collections.values())
            return {
                "db": "in_memory",
                "collections": collections,
                "objects": objects,
                "dataSize": 0,
                "storageSize": 0,
                "ok": 1,
            }
        return {"ok": 1}


def _db_name_from_uri(uri: str) -> str:
    try:
        parsed = urlparse(uri)
        name = parsed.path.strip("/")
        return name or "IMMORTAL"
    except Exception:
        return "IMMORTAL"


def _connect_mongo(uri: str):
    async_client = _mongo_client_(
        uri,
        serverSelectionTimeoutMS=7000,
        connectTimeoutMS=7000,
        socketTimeoutMS=7000,
    )
    sync_client = MongoClient(
        uri,
        serverSelectionTimeoutMS=7000,
        connectTimeoutMS=7000,
        socketTimeoutMS=7000,
    )
    sync_client.admin.command("ping")
    return async_client, sync_client


_mongo_async_ = None
_mongo_sync_ = None
mongodb = None
pymongodb = None

if not config.MONGO_DB_URI:
    LOGGER(__name__).warning(
        "MONGO_DB_URI is missing. Running in in-memory database mode."
    )
    mongodb = _InMemoryDatabase()
    pymongodb = mongodb
else:
    try:
        _mongo_async_, _mongo_sync_ = _connect_mongo(config.MONGO_DB_URI)
        db_name = _db_name_from_uri(config.MONGO_DB_URI)
        mongodb = _mongo_async_[db_name]
        pymongodb = _mongo_sync_[db_name]
        LOGGER(__name__).info(f"MongoDB connected. Using database: {db_name}")
    except Exception as ex:
        LOGGER(__name__).warning(
            f"MongoDB unreachable ({type(ex).__name__}). Switching to in-memory database mode."
        )
        mongodb = _InMemoryDatabase()
        pymongodb = mongodb
