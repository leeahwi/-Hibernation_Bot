import discord
import asyncio
import random
import requests
import pandas as pd
from discord.ext import commands

class userchat:

  def __init__(self, client):
    
    self.client = client


  async def hayong(self,message):
    await message.channel.send(embed=discord.Embed(title="바보하영",colour=0x7289da))


  async def tale(self,message):

      info_user = message.author

      ctx = message.channel
      
      r_num = random.randrange(1,3)

      sent_list = ["길김량","바보멍청이","바보졸개","바보꼬리","멍청이"]
      que_list = ["멍충이인가?","꼬리가 누구야?","먹는거야?"]
      ask_list = ["헤헤... (o´〰`o) 감사해요~ ", "알려줘서 고마워!  ◝(⁰▿⁰)◜ "]


      if r_num == 1:
        
        await ctx.send(embed=discord.Embed(title = None, description = random.choice(sent_list),colour=0x7289da))

      elif r_num == 2:

        await ctx.send(embed=discord.Embed(title = None, description = random.choice(que_list),colour=0x7289da))

        def check(message):
          return message.channel == ctx and message.author == info_user

        try:
          await self.client.wait_for('message', check = check, timeout = 10)

          await ctx.send(embed=discord.Embed(title = None, description = random.choice(ask_list), colour=0x7289da))

        except asyncio.TimeoutError:
          pass

      else:
        print("error")


'''

if message.content.startswith(COMMANDPREFIX+'현구'):
  if message.content[3:] == '':
    await ctx.send(embed=discord.Embed(title="헣",colour=0x7289da))

if message.content.startswith(COMMANDPREFIX+'아휘'):
  if message.content[3:] == '':
    await ctx.send(embed=discord.Embed(title="정상인",colour=0x7289da))

if message.content.startswith(COMMANDPREFIX+'대영'):
  if message.content[3:] == '':
    await ctx.send(embed=discord.Embed(title="야근맨...ㅋ",colour=0x7289da))

if message.content.startswith(COMMANDPREFIX+'호주'):                 
  if message.content[3:] == '':
    await ctx.send(embed=discord.Embed(title="딸내미" + "\N{THUMBS UP SIGN}" ,colour=0x7289da))


if message.content.startswith(COMMANDPREFIX+'시열'):
  if message.content[3:] == '':
    await ctx.send(embed=discord.Embed(title="숄",colour=0x7289da))


if message.content.startswith(COMMANDPREFIX+'감자'):
  if message.content[3:] == '':
    await ctx.send(embed=discord.Embed(title="감자'바보'",colour=0x7289da))


if message.content.startswith(COMMANDPREFIX+'새우'):
  if message.content[3:] == '':
    await ctx.send(embed=discord.Embed(title="^€^",colour=0x7289da))

''' 
