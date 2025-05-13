import traceback

import discord
from discord.ext import commands
import sqlite3


class Multi(commands.Cog):
    _sql_db: sqlite3.Connection

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self._sql_db: sqlite3.Connection = sqlite3.connect(bot.config)

    @commands.command()
    async def start(self, ctx: commands.Context):
        # check if person is registered already and ask if they want to reset
        # otherwise, continue
        await ctx.reply("Not Yet Implemented")

        # first_msg = await ctx.reply("Welcome to The MultiMay bot!\nWould you like to roll daily or weekly?")
        # await first_msg.add_reaction(":one:")
        # await first_msg.add_reaction(":seven:")
        # rate = await self.bot.wait_for("on_reaction_add", check=lambda
        #     x: x.id == first_msg.id and
        #        x.channel.id == first_msg.channel.id and
        #        x.author.id == ctx.author.id)
        # second_msg = await ctx.reply("Okay, and how do you want to determine how many rolls you get?")

    @commands.command()
    async def roll(self, ctx: commands.Context, rolls):
        await ctx.reply("Not Yet Implemented")

    async def cog_load(self) -> None:
        pass

    async def cog_unload(self) -> None:
        try:
            self._sql_db.close()
        except sqlite3.Error:
            pass

class Startup(discord.ui.Modal, title='MultiMay Setup'):
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'You should now be able to roll!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Report this to @paolumu', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)