import discord
import wave
import os
import json
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
from discord.ext import commands, tasks
from enum import Enum
from viperaveil.utilities.Check import Check
from viperaveil import dir_path
import logging
logger = logging.getLogger('discord')

connections = {}

model = Model(lang="en-us")


filters = {
    "time": 4,
    "users": [],
    "max_size": 0
}

# class Sinks(Enum):
#     mp3 = discord.sinks.MP3Sink()
#     wav = discord.sinks.WaveSink()
#     pcm = discord.sinks.PCMSink()
#     ogg = discord.sinks.OGGSink()
#     mka = discord.sinks.MKASink()
#     mkv = discord.sinks.MKVSink()
#     mp4 = discord.sinks.MP4Sink()
#     m4a = discord.sinks.M4ASink()

async def reccallback(sink: discord.sinks.WaveSink, ctx: discord.Interaction):
    channel: discord.TextChannel = ctx.channel
    recorded_users = [f"<@{user_id}>" for user_id, audio in sink.audio_data.items()]
    for user_id, audio in sink.audio_data.items():
        with open(f"{dir_path}/cache/raw-{user_id}.{sink.encoding}", "wb") as f:
            f.write(audio.file.getvalue())
            f.close
        raw_audio = AudioSegment.from_mp3(f"{dir_path}/cache/raw-{user_id}.{sink.encoding}")
        raw_audio = raw_audio.set_channels(1)
        voice_rec = raw_audio.set_sample_width()
        voice_rec.export(f"{dir_path}/cache/{user_id}.{sink.encoding}", format="wav", bitrate="16k")
        wf = wave.open(f"{dir_path}/cache/{user_id}.{sink.encoding}", "rb")
        
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        rec.SetPartialWords(True)
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                print(rec.Result())
            else:
                print(rec.PartialResult())

        phrase = ''
        rec_dict = json.loads(rec.FinalResult())
        for words in rec_dict['result']:
            phrase += ' ' + words['word']

        await ctx.channel.send(
            f"Finished! Recorded audio for {', '.join(recorded_users)}. Phrase was {phrase}", delete_after=12
        )


class voicerecog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @tasks.loop(seconds=4.0)
    # async def recording(self):
    #     """Run voicerec on 4 second loop"""
        


    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    #     if member.id == self.bot.id and after.channel:
    #         bot_voice_client: discord.voice_client.VoiceClient = after.channel.guild.voice_client
    #         for vc in self.bot.voice_clients:
    #             assert vc: discord.voice_client.VoiceClient
    #             if vc.
    #         bot_voice_client.start_recording()
    #         bot_voice_client.

    @discord.slash_command(name="joinrec",
                          description="Add the bot to your voice channel")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def joinrec(self, ctx: discord.Interaction):
        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botNotInVoiceChannel(ctx, self.bot):
            return

        channel = ctx.user.voice.channel

        voiceclient: discord.VoiceClient = await channel.connect()
        connections.update({ctx.guild.id: voiceclient})
        message = await ctx.response.send_message('Recording started', ephemeral=True, delete_after=12)
        voiceclient.start_recording(discord.sinks.MP3Sink(filters=filters), reccallback, ctx)

    @discord.slash_command(name="stoprec")
    async def stoprec(self, ctx: discord.Interaction):
        if ctx.guild.id in connections:
            voiceclient: discord.VoiceClient = connections[ctx.guild.id]
            voiceclient.stop_recording()
            del connections[ctx.guild.id]
            await ctx.response.send_message("Thanks for using this service", delete_after=12)
        else:
            await ctx.response.send_message("Not recording in this guild.", delete_after=12)

def setup(bot):
    bot.add_cog(voicerecog(bot))
