import asyncio
import discord.ext.test as dpytest
import pytest_asyncio
import discord
import discord.ext.commands as commands


@pytest_asyncio.fixture
async def bot():
    intents = discord.Intents.default()
    intents.message_content = True
    b = commands.Bot(command_prefix='!')

async def test_ping():
    bot = ...  # However you create your bot.
    dpytest.configure(bot)
    await dpytest.message("!ping")
    assert dpytest.verify().message().contains().content("Ping:")


async def test_foo():
    bot = ... # Same setup as above
    dpytest.configure(bot)
    await dpytest.message("!hello")
    assert dpytest.verify().message().content("Hello World!")


asyncio.run(test_ping())
asyncio.run(test_foo())