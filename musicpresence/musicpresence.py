import discord
from redbot.core import commands, Config
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("MusicPresence", __file__)


@cog_i18n(_)
class MusicPresence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.config.register_global(
            prefix="Playing:",
            idle_text="Music 24/7",
            idle_type="listening"
        )

    @staticmethod
    def _to_activity_type(activity_type: str) -> discord.ActivityType:
        valid_types = {
            "playing": discord.ActivityType.playing,
            "streaming": discord.ActivityType.streaming,
            "listening": discord.ActivityType.listening,
            "watching": discord.ActivityType.watching,
            "competing": discord.ActivityType.competing,
        }
        return valid_types.get(activity_type.lower(), discord.ActivityType.listening)

    async def update_status(self, text: str, activity_type: str = "listening"):
        activity = discord.Activity(
            type=self._to_activity_type(activity_type),
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
        idle_type = await self.config.idle_type()
        idle = await self.config.idle_text()
        await self.update_status(idle, idle_type)

    @commands.is_owner()
    @commands.group()
    async def mpstatus(self, ctx):
        """Configure the bot status."""
        pass

    @mpstatus.command()
    async def prefix(self, ctx, *, text: str):
        await self.config.prefix.set(text)
        await ctx.send(_("Prefix set: {text}").format(text=text))

    @mpstatus.command()
    async def idle(self, ctx, activity_type: str, *, text: str):
        activity_type = activity_type.lower()
        valid_types = {"playing", "streaming", "listening", "watching", "competing"}
        if activity_type not in valid_types:
            valid_display = ", ".join(sorted(valid_types))
            await ctx.send(
                _("Invalid activity type. Use one of: {types}.").format(types=valid_display)
            )
            return

        await self.config.idle_type.set(activity_type)
        await self.config.idle_text.set(text)
        await ctx.send(_("Idle status updated."))
