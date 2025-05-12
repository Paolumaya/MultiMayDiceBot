from discord.ext import commands


class Multi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx: commands.Context):
        await ctx.reply("Not Yet Implemented")
