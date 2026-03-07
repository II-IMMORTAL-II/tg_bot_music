import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram import errors as pyrogram_errors
from pyrogram.types import InlineKeyboardMarkup

# Newer Pyrogram builds renamed/removed GroupcallForbidden; older PyTgCalls
# still imports this symbol.
if not hasattr(pyrogram_errors, "GroupcallForbidden"):
    pyrogram_errors.GroupcallForbidden = getattr(
        pyrogram_errors,
        "GroupCallInvalid",
        getattr(pyrogram_errors, "Forbidden", Exception),
    )

from pytgcalls import PyTgCalls
try:
    from pytgcalls import StreamType
except Exception:
    StreamType = None
from pytgcalls.exceptions import NoActiveGroupCall
try:
    from pytgcalls.exceptions import AlreadyJoinedError
except Exception:
    try:
        from pytgcalls.exceptions import PyTgCallsAlreadyRunning as AlreadyJoinedError
    except Exception:
        class AlreadyJoinedError(Exception):
            pass
try:
    from pytgcalls.exceptions import NodeJSNotInstalled
except Exception:
    class NodeJSNotInstalled(Exception):
        pass
try:
    from pytgcalls.exceptions import TelegramServerError
except Exception:
    class TelegramServerError(Exception):
        pass
try:
    from pytgcalls.types import (
        MediaStream,
        AudioQuality,
        VideoQuality,
        StreamEnded,
        Update,
    )
    PYTG_NEW_STREAM_API = True
except Exception:
    from pytgcalls.types import Update
    from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
    from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
    from pytgcalls.types.stream import StreamAudioEnded as StreamEnded
    PYTG_NEW_STREAM_API = False

import config
from IMMORTAL_MUSIC import LOGGER, YouTube, app
from IMMORTAL_MUSIC.misc import db
from IMMORTAL_MUSIC.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from IMMORTAL_MUSIC.utils.exceptions import AssistantErr
from IMMORTAL_MUSIC.utils.formatters import check_duration, seconds_to_min, speed_converter
from IMMORTAL_MUSIC.utils.inline.play import stream_markup, telegram_markup
from IMMORTAL_MUSIC.utils.stream.autoclear import auto_clean
from IMMORTAL_MUSIC.utils.thumbnails import get_thumb
from strings import get_string

autoend = {}
counter = {}


async def _clear_(chat_id):
    queued = db.get(chat_id, [])
    for item in queued:
        await auto_clean(item)
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


class Call(PyTgCalls):
    @staticmethod
    def _is_supported_client(client) -> bool:
        return all(
            hasattr(client, method_name)
            for method_name in ("join_group_call", "change_stream", "leave_group_call")
        )

    async def _require_supported_client(self, assistant):
        if self._is_supported_client(assistant):
            return
        raise AssistantErr(
            "Incompatible PyTgCalls build detected. Install py-tgcalls==0.9.7 "
            "and run this project on Python 3.10/3.11."
        )

    @staticmethod
    def _build_stream(source, video=False, ffmpeg_params=None):
        if PYTG_NEW_STREAM_API:
            kwargs = {"audio_parameters": AudioQuality.HIGH}
            if video:
                kwargs["video_parameters"] = VideoQuality.SD_480p
            if ffmpeg_params:
                kwargs["additional_ffmpeg_parameters"] = ffmpeg_params
            return MediaStream(source, **kwargs)

        kwargs = {}
        if ffmpeg_params:
            kwargs["additional_ffmpeg_parameters"] = ffmpeg_params
        if video:
            return AudioVideoPiped(
                source,
                audio_parameters=HighQualityAudio(),
                video_parameters=MediumQualityVideo(),
                **kwargs,
            )
        return AudioPiped(
            source,
            audio_parameters=HighQualityAudio(),
            **kwargs,
        )

    def __init__(self):
        self.userbot1 = Client(
            name="IMMORTALAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(
            self.userbot1,
            cache_duration=100,
        )
        self.userbot2 = Client(
            name="IMMORTALAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.two = PyTgCalls(
            self.userbot2,
            cache_duration=100,
        )
        self.userbot3 = Client(
            name="IMMORTALXAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.three = PyTgCalls(
            self.userbot3,
            cache_duration=100,
        )
        self.userbot4 = Client(
            name="IMMORTALXAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )
        self.four = PyTgCalls(
            self.userbot4,
            cache_duration=100,
        )
        self.userbot5 = Client(
            name="IMMORTALAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )
        self.five = PyTgCalls(
            self.userbot5,
            cache_duration=100,
        )

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await self._require_supported_client(assistant)
        try:
            await _clear_(chat_id)
            await assistant.leave_group_call(chat_id)
        except:
            pass

    async def stop_stream_force(self, chat_id: int):
        try:
            if config.STRING1:
                await self.one.leave_group_call(chat_id)
        except:
            pass
        try:
            if config.STRING2:
                await self.two.leave_group_call(chat_id)
        except:
            pass
        try:
            if config.STRING3:
                await self.three.leave_group_call(chat_id)
        except:
            pass
        try:
            if config.STRING4:
                await self.four.leave_group_call(chat_id)
        except:
            pass
        try:
            if config.STRING5:
                await self.five.leave_group_call(chat_id)
        except:
            pass
        try:
            await _clear_(chat_id)
        except:
            pass

    async def speedup_stream(self, chat_id: int, file_path, speed, playing):
        assistant = await group_assistant(self, chat_id)
        await self._require_supported_client(assistant)
        if str(speed) != str("1.0"):
            base = os.path.basename(file_path)
            chatdir = os.path.join(os.getcwd(), "playback", str(speed))
            if not os.path.isdir(chatdir):
                os.makedirs(chatdir)
            out = os.path.join(chatdir, base)
            if not os.path.isfile(out):
                if str(speed) == str("0.5"):
                    vs = 2.0
                if str(speed) == str("0.75"):
                    vs = 1.35
                if str(speed) == str("1.5"):
                    vs = 0.68
                if str(speed) == str("2.0"):
                    vs = 0.5
                proc = await asyncio.create_subprocess_shell(
                    cmd=(
                        "ffmpeg "
                        "-i "
                        f"{file_path} "
                        "-filter:v "
                        f"setpts={vs}*PTS "
                        "-filter:a "
                        f"atempo={speed} "
                        f"{out}"
                    ),
                    stdin=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await proc.communicate()
            else:
                pass
        else:
            out = file_path
        dur = await asyncio.get_running_loop().run_in_executor(None, check_duration, out)
        dur = int(dur)
        played, con_seconds = speed_converter(playing[0]["played"], speed)
        duration = seconds_to_min(dur)
        stream = self._build_stream(
            out,
            video=playing[0]["streamtype"] == "video",
            ffmpeg_params=f"-ss {played} -to {duration}",
        )
        if str(db[chat_id][0]["file"]) == str(file_path):
            await assistant.change_stream(chat_id, stream)
        else:
            raise AssistantErr("Umm")
        if str(db[chat_id][0]["file"]) == str(file_path):
            exis = (playing[0]).get("old_dur")
            if not exis:
                db[chat_id][0]["old_dur"] = db[chat_id][0]["dur"]
                db[chat_id][0]["old_second"] = db[chat_id][0]["seconds"]
            db[chat_id][0]["played"] = con_seconds
            db[chat_id][0]["dur"] = duration
            db[chat_id][0]["seconds"] = dur
            db[chat_id][0]["speed_path"] = out
            db[chat_id][0]["speed"] = speed

    async def force_stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await self._require_supported_client(assistant)
        try:
            check = db.get(chat_id)
            check.pop(0)
        except:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except:
            pass

    async def skip_stream(
        self,
        chat_id: int,
        link: str,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        await self._require_supported_client(assistant)
        stream = self._build_stream(link, video=bool(video))
        await assistant.change_stream(
            chat_id,
            stream,
        )

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        assistant = await group_assistant(self, chat_id)
        await self._require_supported_client(assistant)
        stream = self._build_stream(
            file_path,
            video=(mode == "video"),
            ffmpeg_params=f"-ss {to_seek} -to {duration}",
        )
        await assistant.change_stream(chat_id, stream)

    async def stream_call(self, link):
        assistant = await group_assistant(self, config.LOGGER_ID)
        await self._require_supported_client(assistant)
        kwargs = {}
        if StreamType:
            kwargs["stream_type"] = StreamType().pulse_stream
        await assistant.join_group_call(
            config.LOGGER_ID,
            self._build_stream(link, video=True),
            **kwargs,
        )
        await asyncio.sleep(0.2)
        await assistant.leave_group_call(config.LOGGER_ID)

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        await self._require_supported_client(assistant)
        language = await get_lang(chat_id)
        _ = get_string(language)
        stream = self._build_stream(link, video=bool(video))
        try:
            kwargs = {}
            if StreamType:
                kwargs["stream_type"] = StreamType().pulse_stream
            await assistant.join_group_call(
                chat_id,
                stream,
                **kwargs,
            )
        except NoActiveGroupCall:
            raise AssistantErr(_["call_8"])
        except AlreadyJoinedError:
            raise AssistantErr(_["call_9"])
        except TelegramServerError:
            raise AssistantErr(_["call_10"])
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        if await is_autoend():
            counter[chat_id] = {}
            users = len(await assistant.get_participants(chat_id))
            if users == 1:
                autoend[chat_id] = datetime.now() + timedelta(minutes=1)

    async def change_stream(self, client, chat_id):
        check = db.get(chat_id)
        popped = None
        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop = loop - 1
                await set_loop(chat_id, loop)
            await auto_clean(popped)
            if not check:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)
        except:
            try:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)
            except:
                return
        else:
            queued = check[0]["file"]
            language = await get_lang(chat_id)
            _ = get_string(language)
            title = (check[0]["title"]).title()
            user = check[0]["by"]
            original_chat_id = check[0]["chat_id"]
            streamtype = check[0]["streamtype"]
            videoid = check[0]["vidid"]
            db[chat_id][0]["played"] = 0
            exis = (check[0]).get("old_dur")
            if exis:
                db[chat_id][0]["dur"] = exis
                db[chat_id][0]["seconds"] = check[0]["old_second"]
                db[chat_id][0]["speed_path"] = None
                db[chat_id][0]["speed"] = 1.0
            video = True if str(streamtype) == "video" else False
            if "live_" in queued:
                n, link = await YouTube.video(videoid, True)
                if n == 0:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_6"],
                    )
                stream = self._build_stream(link, video=video)
                try:
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_6"],
                    )
                img = await get_thumb(videoid)
                button = telegram_markup(_, chat_id)
                run = await app.send_photo(
                    chat_id=original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        title[:23],
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif "vid_" in queued:
                mystic = await app.send_message(original_chat_id, _["call_7"])
                try:
                    file_path, direct = await YouTube.download(
                        videoid,
                        mystic,
                        videoid=True,
                        video=True if str(streamtype) == "video" else False,
                    )
                except:
                    try:
                        file_path, direct = await YTB.download(
                            videoid,
                            mystic,
                            videoid=True,
                            video=True if str(streamtype) == "video" else False,
                        )
                    except:
                        return await mystic.edit_text(
                            _["call_6"], disable_web_page_preview=True
                        )
                stream = self._build_stream(file_path, video=video)
                try:
                    await client.change_stream(chat_id, stream)
                except:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_6"],
                    )
                img = await get_thumb(videoid)
                button = stream_markup(_, videoid, chat_id)
                await mystic.delete()
                run = await app.send_photo(
                    chat_id=original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        title[:23],
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
            elif "index_" in queued:
                stream = self._build_stream(videoid, video=(str(streamtype) == "video"))
                try:
                    await client.change_stream(chat_id, stream)
                except:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_6"],
                    )
                button = telegram_markup(_, chat_id)
                run = await app.send_photo(
                    chat_id=original_chat_id,
                    photo=config.STREAM_IMG_URL,
                    caption=_["stream_2"].format(user),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                stream = self._build_stream(queued, video=video)
                try:
                    await client.change_stream(chat_id, stream)
                except:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_6"],
                    )
                if videoid == "telegram":
                    button = telegram_markup(_, chat_id)
                    run = await app.send_photo(
                        chat_id=original_chat_id,
                        photo=(
                            config.TELEGRAM_AUDIO_URL
                            if str(streamtype) == "audio"
                            else config.TELEGRAM_VIDEO_URL
                        ),
                        caption=_["stream_1"].format(
                            config.SUPPORT_CHAT, title[:23], check[0]["dur"], user
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"
                elif videoid == "soundcloud":
                    button = telegram_markup(_, chat_id)
                    run = await app.send_photo(
                        chat_id=original_chat_id,
                        photo=config.SOUNCLOUD_IMG_URL,
                        caption=_["stream_1"].format(
                            config.SUPPORT_CHAT, title[:23], check[0]["dur"], user
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"
                else:
                    img = await get_thumb(videoid)
                    button = stream_markup(_, videoid, chat_id)
                    run = await app.send_photo(
                        chat_id=original_chat_id,
                        photo=img,
                        caption=_["stream_1"].format(
                            f"https://t.me/{app.username}?start=info_{videoid}",
                            title[:23],
                            check[0]["dur"],
                            user,
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "stream"

    async def ping(self):
        pings = []
        if config.STRING1:
            pings.append(await self.one.ping)
        if config.STRING2:
            pings.append(await self.two.ping)
        if config.STRING3:
            pings.append(await self.three.ping)
        if config.STRING4:
            pings.append(await self.four.ping)
        if config.STRING5:
            pings.append(await self.five.ping)
        return str(round(sum(pings) / len(pings), 3))

    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Client...\n")
        if not self._is_supported_client(self.one):
            LOGGER(__name__).error(
                "Incompatible PyTgCalls API loaded. "
                "Expected legacy API used by this project. "
                "Install py-tgcalls==0.9.7 and use Python 3.10/3.11."
            )
        async def _start_client(name, client):
            try:
                await client.start()
            except NodeJSNotInstalled:
                LOGGER(__name__).error(
                    f"{name} could not start: Node.js is not installed in this runtime. "
                    "Install Node.js 15+ (recommended 18+) and redeploy."
                )

        if config.STRING1:
            await _start_client("Assistant 1", self.one)
        if config.STRING2:
            await _start_client("Assistant 2", self.two)
        if config.STRING3:
            await _start_client("Assistant 3", self.three)
        if config.STRING4:
            await _start_client("Assistant 4", self.four)
        if config.STRING5:
            await _start_client("Assistant 5", self.five)

    async def decorators(self):
        assistants = [self.one, self.two, self.three, self.four, self.five]
        if all(hasattr(assistant, "on_stream_end") for assistant in assistants):
            @self.one.on_kicked()
            @self.two.on_kicked()
            @self.three.on_kicked()
            @self.four.on_kicked()
            @self.five.on_kicked()
            @self.one.on_closed_voice_chat()
            @self.two.on_closed_voice_chat()
            @self.three.on_closed_voice_chat()
            @self.four.on_closed_voice_chat()
            @self.five.on_closed_voice_chat()
            @self.one.on_left()
            @self.two.on_left()
            @self.three.on_left()
            @self.four.on_left()
            @self.five.on_left()
            async def stream_services_handler(_, chat_id: int):
                await self.stop_stream(chat_id)

            @self.one.on_stream_end()
            @self.two.on_stream_end()
            @self.three.on_stream_end()
            @self.four.on_stream_end()
            @self.five.on_stream_end()
            async def stream_end_handler1(client, update: Update):
                if not isinstance(update, StreamEnded):
                    return
                await self.change_stream(client, update.chat_id)
        elif all(hasattr(assistant, "on_update") for assistant in assistants):
            @self.one.on_update()
            @self.two.on_update()
            @self.three.on_update()
            @self.four.on_update()
            @self.five.on_update()
            async def stream_end_handler2(client, update: Update):
                if isinstance(update, StreamEnded):
                    await self.change_stream(client, update.chat_id)
        else:
            LOGGER(__name__).warning(
                "PyTgCalls decorators are unavailable in this runtime. "
                "Stream lifecycle hooks were not registered."
            )


IMMORTAL = Call()


