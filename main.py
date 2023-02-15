import io

import aiohttp
import discord
import os
import sys
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
EMOJI_SOURCE = int(os.getenv('EMOJI_SOURCE'))
EMOJI_DEST = int(os.getenv('EMOJI_DEST'))

intents = discord.Intents.default()
client = discord.Client(intents=intents)


def list_servers():
    print(f'{client.user} is connected to the following servers:')

    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')

async def clone_emojis():
    source = client.get_guild(EMOJI_SOURCE)
    dest = client.get_guild(EMOJI_DEST)

    async with aiohttp.ClientSession() as session:
        for emoji in source.emojis:
            async with session.get(emoji.url) as resp:
                if resp.status != 200:
                    print(f'Something went wrong retrieving {emoji.name}')
                image = await resp.read()
                await dest.create_custom_emoji(name=emoji.name, image=image)

            print(f'Successfully duplicated emoji {emoji.name}')

async def clear_dest():
    dest = client.get_guild(EMOJI_DEST)

    for emoji in dest.emojis:
        await dest.delete_emoji(emoji)
        print(f'deleted {emoji.name}')

functions = {
    'list_servers': list_servers,
    'clone_emojis': clone_emojis,
    'clear_dest': clear_dest
}


@client.event
async def on_ready():
    try:
        functions[sys.argv[1]]()
    except IndexError:
        print(f'Needs a parameter; options are {list(functions.keys())}')
    except KeyError:
        print(f'Invalid parameter; options are {list(functions.keys())}')

    print('\nThanks to Windows, close this manually or be spammed with a stack trace')

client.run(token=TOKEN)
