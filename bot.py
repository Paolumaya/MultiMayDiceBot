import json
import base64
import sqlite3
from typing import Optional
import zlib
from urllib.parse import unquote

import discord
import tomlkit
from discord import app_commands
import traceback
from pprint import pp

from discord.utils import MISSING


class MultiClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
intents.message_content = True

MY_GUILD = discord.Object(id=245674056760819712)

client = MultiClient(intents=intents)


@client.event
async def on_ready():
    print("ready")


@client.event
async def on_message(message: discord.Message):
    if str(message.channel.id) != config['webhook_channel']:
        print(message.content)
        # print(message.channel.id)
        return
    obfuscated_info = message.content.encode()
    zipped_info = base64.decodebytes(obfuscated_info)
    unzipped_info = zlib.decompress(zipped_info)
    readable_info = unquote(unzipped_info, 'utf-8')
    pp(json.loads(readable_info))


# @client.tree.command()
# async def roll(interaction: discord.Interaction):
#     z = await interaction.response.send_message("asdf", ephemeral=True)
#     print(type(z))
#     print(dir(z))
#     print(z)


def load_config() -> dict:
    default = {'token': '', 'sql_file': 'multi.sql', 'webhook_channel': '1372438452129239040'}

    try:
        with open('config.toml') as cfg:
            dd_config = tomlkit.load(cfg)
            for k1, v1 in default.items():
                if k1 not in dd_config.keys():
                    dd_config[k1] = v1
                if isinstance(v1, dict):
                    for k2, v2 in v1.items():
                        if k2 not in dd_config[k1].keys():
                            dd_config[k1][k2] = v2

        with open('config.toml', 'w') as cfg2:
            tomlkit.dump(dd_config, cfg2)
        return dd_config
    except FileNotFoundError:
        with open('config.toml', 'w+') as cfg3:
            tomlkit.dump(default, cfg3)
        return default.copy()


config = load_config()
conn = sqlite3.connect(config["sql_file"])
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS multi (
user_name TEXT
user_id TEXT

roll_cooldown INTEGER
last_roll_timestamp INTEGER
roll_count_column TEXT

clones INTEGER
torsos INTEGER
taursos INTEGER 
heads INTEGER
eyes INTEGER
snouts INTEGER
mouths INTEGER
tongues INTEGER
arms INTEGER
fingers INTEGER
thumbs INTEGER
legs INTEGER
toes INTEGER
custom_things TEXT
)""")
client.run(config["token"])
