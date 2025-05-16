import base64
import hashlib
import json
import re
import sqlite3
import zlib
from pprint import pp
from urllib.parse import unquote

import discord
import tomlkit
from discord import app_commands


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


valid = re.compile(
    r'^(code)|(roll_freq)|(inst_part)|(affect)|(n_body)|(are_each_named)|(are_different)|(main_body_name)|(t_name)\d+|(c_torso)\d+|(n_torso)\d+|(c_taurso)\d+|(n_taurso)\d+|(c_head)\d+|(n_head)\d+|(c_eye)\d+|(n_eye)\d+|(c_pupil)\d+|(n_pupil)\d+|(c_snout)\d+|(n_snout)\d+|(c_nose)\d+|(n_nose)\d+|(c_nostril)\d+|(n_nostril)\d+|(c_mouth)\d+|(n_mouth)\d+|(c_tooth)\d+|(n_tooth)\d+|(c_tongue)\d+|(n_tongue)\d+|(c_arm)\d+|(n_arm)\d+|(c_hand)\d+|(n_hand)\d+|(c_thumb)\d+|(n_thumb)\d+|(c_finger)\d+|(n_finger)\d+|(c_tail)\d+|(n_tail)\d+|(c_leg)\d+|(n_leg)\d+|(c_foot)\d+|(n_foot)\d+|(c_toe)\d+|(n_toe)\d+$')

# use this later idiot https://www.liquid-technologies.com/online-json-to-schema-converter

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
    usable_info = json.loads(readable_info)
    pp(usable_info)

    bad_keys = []
    failed = False
    for k, v in usable_info.items():
        match = re.match(valid, k)
        if not match:
            failed = True
            bad_keys.append(k)

    if failed:
        await message.channel.send(
            content=f'INVALID KEYS `{", ".join(bad_keys)}`! THIS MESSAGE HAS BEEN TAMPERED WITH!', reference=message)
        return




def encode(text: bytes | str) -> str:
    if isinstance(text, str):
        secret = hashlib.sha256(config['salt'].encode() + text.encode()).hexdigest()
    else:
        secret = hashlib.sha256(config['salt'].encode() + text).hexdigest()
    return secret


@client.tree.command()
async def roll(interaction: discord.Interaction):
    interaction.user.id
    z = await interaction.response.send_message("asdf", ephemeral=True)
    print(type(z))
    print(dir(z))
    print(z)


@client.tree.command()
async def setup(interaction: discord.Interaction):
    secret = encode(str(interaction.user.id))
    # pp(secret)

    await interaction.response.send_message(secret, ephemeral=True)


default_cfg = {'token': '',
               'sql_file': 'multi.sql',
               'webhook_channel': '1372438452129239040',
               'salt': ''}


def load_config() -> dict:
    try:
        with open('config.toml') as cfg:
            dd_config = tomlkit.load(cfg)
            for k1, v1 in default_cfg.items():
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
            tomlkit.dump(default_cfg, cfg3)
        return default_cfg.copy()


def save_config() -> bool:
    try:
        with open('config.toml') as cfg:
            global config
            disk_config = tomlkit.load(cfg)
            for k1, v1 in config.items():
                if k1 not in disk_config.keys():
                    disk_config[k1] = v1
                if isinstance(v1, dict):
                    for k2, v2 in v1.items():
                        if k2 not in disk_config[k1].keys():
                            disk_config[k1][k2] = v2
            with open('config.toml', 'w') as cfg2:
                tomlkit.dump(disk_config, cfg2)
            return True
    except FileNotFoundError:
        print('what')
        return False


if __name__ == '__main__':
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
