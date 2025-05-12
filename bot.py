import discord
import tomlkit

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("ready")


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
client.run(config["token"])
