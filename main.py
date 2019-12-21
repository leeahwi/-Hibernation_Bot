import discord
import os

from discord.ext import commands
#from settings import *

TOKEN = os.environ['BOT_TOKEN']
#TOKEN = 'repl token'

client = discord.Client()

#bot = commands.Bot(command_prefix = '$')

COMMANDPREFIX = '!'

@client.event
async def on_ready():
    print('Logged in...')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))
  #check it work

@client.event
async def on_message(message):
  ctx = message.channel
  
  if message.author == client.user:
      return
  #do not react if author == bot
  #check it work
  
  if message.content == 'test2':
      await message.channel.send("test2")
  #check it work
 
  if message.content.startswith(COMMANDPREFIX+'test'):
      #print(ctx)
      #print(message.channel)
      await message.channel.send("test3")
      msg = message.content[6:]
      #print(str(msg))
      #await ctx.send(msg)
      await ctx.send(message.author)
      await ctx.send(message.author.id)
      await ctx.send(client.user)

  #메세지 삭제, 사용자와 봇 메세지 까지 삭제 확인
  if message.content.startswith(COMMANDPREFIX+'delete'):
     # msgd = before.message
      await message.delete(delay=1)
      message = await ctx.send("delete checking")
      await message.delete(delay=1)
  #check it work
 
  #봇 상태 바꾸기(추후에 온오프라인, 다른 용무중도 바꿀예정)
  if message.content.startswith(COMMANDPREFIX+'status'):
      msg = message.content[8:]
      await client.change_presence(activity=discord.Game(name=msg))
      await ctx.send("done")
    #check it work

  #check it work




'''
@bot.command
async def test():
   await message.channel.send("test")

@bot.event
async def on_message(message):
    await message.channel.send("hello!")
'''


client.run(TOKEN)
