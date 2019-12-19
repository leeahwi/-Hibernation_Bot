import discord
import os

client = discord.Client()

TOKEN = os.environ('BOT_TOKEN')

@client.event
async def on_ready():
    print('Logged in...')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))

client.run(TOKEN)
