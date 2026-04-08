import discord
from redbot.core import commands, Config


class MusicPresence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.config.register_global(
            prefix="Playing:",
            idle_text="Music 24/7",
            idle_type="listening"
        )

    async def update_status(self, text):
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name=text[:120]
        )
        await self.bot.change_presence(activity=activity)

    @commands.Cog.listener()
    async def on_red_audio_track_start(self, guild, track, requester):
        prefix = await self.config.prefix()

        title = getattr(track, "title", "Music")
        author = getattr(track, "author", "")

        name = f"{title} - {author}" if author else title

        await self.update_status(f"{prefix} {name}")

    @commands.Cog.listener()
    async def on_red_audio_track_end(self, guild, track, requester):
        idle = await self.config.idle_text()
        await self.update_status(idle)

    @commands.is_owner()
    @commands.group()
    async def mpstatus(self, ctx):
        """Configure the bot status"""
        pass

    @mpstatus.command()
    async def prefix(self, ctx, *, text: str):
        await self.config.prefix.set(text)
        await ctx.send(f"Prefix set: {text}")

    @mpstatus.command()
    async def idle(self, ctx, activity_type: str, *, text: str):
        await self.config.idle_type.set(activity_type)
        await self.config.idle_text.set(text)
        await ctx.send("Idle status updated")