import sqlite3
from typing import Optional

import discord
import tomlkit
from discord import app_commands
import traceback

from discord.utils import MISSING


class MultiClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


class Startup(discord.ui.Modal):
    def __init__(self, *, title: str = MISSING, timeout: Optional[float] = None, custom_id: str = MISSING) -> None:
        super().__init__(title=title, custom_id=custom_id, timeout=timeout)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Report this to @paolumu.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)

    async def on_timeout(self) -> None:
        pass



class StartupCore(Startup, title='Core Body Parts'):
    cnt_clone = discord.ui.TextInput(label="# of Individual Bodies", placeholder="enter a number", default="1")
    cnt_torso = discord.ui.TextInput(label="# of Upper Bodies", placeholder="enter a number", default="1")
    cnt_taurso = discord.ui.TextInput(label="# of Lower Bodies ('Taursos')", placeholder="enter a number", default="1")

    async def on_submit(self, interaction: discord.Interaction):
        print(self.cnt_clone)
        print(self.cnt_torso)
        print(self.cnt_taurso)
        await interaction.response.send_message("Okay! Now run `/setup2`!", ephemeral=True)


class StartupHead(Startup, title='Usually-Head-Related Parts'):
    cnt_head = discord.ui.TextInput(label="# of Heads", placeholder="enter a number", default="1")
    cnt_eye = discord.ui.TextInput(label="# of Eyes", placeholder="enter a number", default="2")
    cnt_snout = discord.ui.TextInput(label="# of Snouts", placeholder="enter a number", default="1")
    cnt_mouth = discord.ui.TextInput(label="# of Mouths", placeholder="enter a number", default="1")
    cnt_tongue = discord.ui.TextInput(label="# of Tongues", placeholder="enter a number", default="1")

    async def on_submit(self, interaction: discord.Interaction):
        print(self.cnt_head)
        print(self.cnt_eye)
        print(self.cnt_snout)
        print(self.cnt_mouth)
        print(self.cnt_tongue)
        await interaction.response.send_message("Almost Done! Now run `/setup3`!", ephemeral=True)


class StartupExtremities(Startup, title='Extremities'):
    cnt_arm = discord.ui.TextInput(label="# of Arms", placeholder="enter a number", default="2")
    cnt_finger = discord.ui.TextInput(label="# of Fingers per hand", placeholder="enter a number", default="5")
    cnt_leg = discord.ui.TextInput(label="# of Legs", placeholder="enter a number", default="2")
    cnt_toe = discord.ui.TextInput(label="# of Toes per foot", placeholder="enter a number", default="5")

    async def on_submit(self, interaction: discord.Interaction):
        print(self.cnt_arm)
        print(self.cnt_finger)
        print(self.cnt_leg)
        print(self.cnt_toe)
        # cur.execute()
        await interaction.response.send_message(f'You should now be able to roll using `/roll`!', ephemeral=True)


intents = discord.Intents.default()
intents.message_content = True

MY_GUILD = discord.Object(id=245674056760819712)

client = MultiClient(intents=intents)


# client.tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("ready")


@client.tree.command()
async def setup1(interaction: discord.Interaction):
    # x = await interaction.response.send_modal(StartupCore())
    await interaction.response.send_modal(StartupCore())
    # print(type(x))
    # print(dir(x))
    # print(x)


@client.tree.command()
async def setup2(interaction: discord.Interaction):
    y = await interaction.response.send_modal(StartupHead())
    print(type(y))
    print(dir(y))
    print(y)


@client.tree.command()
async def setup3(interaction: discord.Interaction):
    z = await interaction.response.send_modal(StartupExtremities())
    print(type(z))
    print(dir(z))
    print(z)


def load_config() -> dict:
    default = {'token': '', 'sql_file': 'multi.sql'}

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
legs INTEGER
toes INTEGER
custom_things TEXT
)""")
client.run(config["token"])
