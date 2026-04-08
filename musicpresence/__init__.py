from .musicpresence import MusicPresence

async def setup(bot):
    await bot.add_cog(MusicPresence(bot))