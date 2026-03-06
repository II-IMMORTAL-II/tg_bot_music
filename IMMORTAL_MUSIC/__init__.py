from IMMORTAL_MUSIC.core.bot import NOBITA
from IMMORTAL_MUSIC.core.dir import dirr
from IMMORTAL_MUSIC.core.git import git
from IMMORTAL_MUSIC.core.userbot import Userbot
from IMMORTAL_MUSIC.misc import dbb, heroku

from SafoneAPI import SafoneAPI
from .logger import LOGGER

dirr()
git()
dbb()
heroku()

app = NOBITA()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

