import sqlite3

conn = sqlite3.connect('test.sql')
cur = conn.cursor()

table_defs = {'settings': ('user_id', 'roll_cooldown', 'last_roll_timestamp', 'individuality', 'change_affects',
                           'separate_names',
                           'enable_torso', 'enable_taurso',
                           'enable_head', 'enable_eye', 'enable_pupil',
                           'enable_snout', 'enable_nose', 'enable_nostril',
                           'enable_mouth', 'enable_tooth', 'enable_tongue',
                           'enable_arm', 'enable_hand', 'enable_thumb', 'enable_finger',
                           'enable_tail', 'enable_leg', 'enable_foot', 'enable_toe',),

              'bodies': ('user_id', 'body_id', 'parent_body_id',
                         'name',
                         'torso', 'taurso',
                         'head', 'eye', 'pupil',
                         'snout', 'nose', 'nostril',
                         'mouth', 'tooth', 'tongue',
                         'arm', 'hand', 'thumb', 'finger',
                         'tail', 'leg', 'foot', 'toe',
                         'custom'),

              'setup_temp': ('user_id', 'register_timestamp', 'secret'), }

for k,v in table_defs.items():
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {k}({', '.join(table_defs[k])})""")


table = 'bodies'
pp = f"""INSERT INTO {table} VALUES"""

# cur.execute("""CREATE TABLE IF NOT EXISTS settings(user_id, roll_cooldown, last_roll_timestamp, )""")


# cur.execute("""CREATE TABLE IF NOT EXISTS settings(user_id, roll_cooldown, last_roll_timestamp, )""")

# cur.execute("""CREATE TABLE IF NOT EXISTS multi (
# user_name TEXT
# user_id TEXT
#
# roll_cooldown INTEGER
# last_roll_timestamp INTEGER
# roll_count_column TEXT
#
# clones INTEGER
# torsos INTEGER
# taursos INTEGER
# heads INTEGER
# eyes INTEGER
# snouts INTEGER
# mouths INTEGER
# tongues INTEGER
# arms INTEGER
# fingers INTEGER
# thumbs INTEGER
# legs INTEGER
# toes INTEGER
# custom_things TEXT
# )""")
