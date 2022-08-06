## Class to handle information about individual tracks
import boilerBot.lib as lib
from common import ytdlhandler
import discord
class Track():
    def __init__(self):
        self.handler = None
        self.title = None
        self.restricted = False

    async def _init(self, searchterm, bot, guild):
        self.handler = await ytdlhandler.ytdlSrc.from_url(searchterm, bot,guild, loop=bot.loop,stream=True)
        if not self.handler:
            self.restricted = True
        self.title = self.handler.title

    async def play(self, player, guild, after):
        try:
            player.voiceclient.play(self.handler,after=lambda e: after(guild))
        except discord.ClientException as er:
            if er.args[0] == 'Already playing audio.':
                player.addtoqueue(self)
                return lib.embed(
                    title = "Track added to queue",
                    description = self.title
                )
        else:
            return lib.embed(
                title = "Now playing:",
                description = self.title
            )
