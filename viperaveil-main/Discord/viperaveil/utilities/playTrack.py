from viperaveil.utilities.database.Queue import DBQueue
from viperaveil.utilities.youtube_dl import ydlLookup
from viperaveil.utilities.sendPlayingSongEmbed import sendPlayingSongEmbed
import discord
import wavelink

import logging
logger = logging.getLogger('discord')


class Track(wavelink.Track):
    """Wavelink Track object with a requester attribute."""

    __slots__ = ('requester', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get('requester')
        self.thumb = kwargs.get('thumb')


async def playTrack(self, ctx: discord.Interaction, player: wavelink.Player, track, requester):
    if player.is_playing():
        return

    if isinstance(track, str):
        # Convert the link in a track
        track: wavelink.Track = await self.bot.wavelink.get_tracks(cls=wavelink.Track, query=track)
        track = track[0]
        if track is None:
            return await ctx.channel.send(f"{self.bot.emoji_list.false} The song link is invalid!")
    if not hasattr(track, 'thumb'):
        new_track = DBQueue(self.bot.db_connection).getCurrentSong(ctx.guild.id)
        try:
            track.thumb = new_track[9]
        except:
            pass
        if not track.thumb:
            try:
                ydltrack = await ydlLookup(track.uri)
                track.thumb = ydltrack['thumbnail']
            except BaseException:
                track.thumb = 'https://www.viperaveil.net/static/images/logo192.png'

    # Add the requester
    track = Track(track.id, track.info, requester=requester, thumb=track.thumb)

    await player.play(track)

    # Send the embed
    await sendPlayingSongEmbed(self, ctx, track)
