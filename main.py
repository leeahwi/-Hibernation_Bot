import discord
import asyncio
import youtube_dl
import requests
import os

from features import *

TOKEN = os.environ('BOT_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='#')

@client.event
async def on_ready():
    print('Logged in...')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))

client.run(TOKEN)
