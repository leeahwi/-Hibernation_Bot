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


@bot.command()
async def join():
 if message.author.voice_channel != None and client.is_voice_connected(message.server) != True:
                global currentChannel
                global player
                global voice
                currentChannel = client.get_channel(message.author.voice_channel.id)
                voice = await client.join_voice_channel(currentChannel)

            elif message.author.voice_channel == None:
                await client.send_message(message.channel, '절 부른 사람이 음성채널에 없어요..')

            else:
                await client.send_message(message.channel, '이미 들왔어!')

client.run(TOKEN)
