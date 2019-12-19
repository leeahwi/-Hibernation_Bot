import discord
import os

from discord.ext import commands

client = discord.Client()

TOKEN = os.environ['BOT_TOKEN']
bot = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print('Logged in...')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))

@bot.command
async def test():
  await message.channel.send("test")

client.run(TOKEN)
