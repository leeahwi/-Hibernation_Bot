import discord
import asyncio
import os
import aiohttp
import io
import random

import requests
import numpy as np
import pandas as pd
import json
import datetime as dt

#내가 만들 모듈
from prac import *

from pytz import timezone
from discord.ext import commands
from collections import Counter

TOKEN = os.environ['BOT_TOKEN']
cyp_TOKEN = os.environ['CYP_TOKEN']


client = commands.Bot(command_prefix="$")

@client.event
async def on_ready():
    print('Logged in...')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))

  #봇 상태 바꾸기
    botActivity = discord.Activity(name= "겨울 보내기", type=discord.ActivityType.playing)
    await client.change_presence(activity=botActivity)
  #check it work



@client.command()
async def test(message):
  
  #기본 변수
  info_user = message.author
  ctx = message.channel

  await ctx.send("testing")

us_chat = userchat(client)

@client.command()
async def 꼬리(message):
  await us_chat.tale(message)

@client.command()
async def 하영(message):
  await us_chat.hayong(message)

@client.command()
async def 팀배정(message):
  await divide_team(message)

@client.command()
async def 전적(message):
  await search_cypdata(message,cyp_TOKEN)

#메세지 단일 또는 다중 삭제
@client.command()
async def delete(msg):

  #기본 변수
  info_user = msg.author
  ctx = msg.channel
  che = False
  
  #msg = message.content[8:] -> error
  #msg = msg.message.content[8:] -> done
  
  msg = msg.message.content[8:]
  
  
  print(msg)

  #메세지 삭제 함수
  async def del_message(num,info_user):

    counter = 0

    #삭제할 메세지 갯수
    number = num 

    #가져올 메세지의 조건
    def predicate(message):
      return not message.author.bot #not bot message

    #최근 200개의 메세지 중 조건에 맞는 메세지 삭제
    #message -> 메세지
    #number -> 삭제할 갯수
    #info_user -> 명령어 호출한 유저

    async for message in ctx.history(limit=200).filter(predicate):

      #메세지의 user가 명령어 호출한 유저와 같은지 확인
      if message.author == info_user:
        
        await message.delete(delay=0)

        await asyncio.sleep(1.0)

        counter += 1

      #정해진 갯수의 메세지 삭제 후
      if counter == number:
        return True
        break



  # msg에 입력된 값이 없을경우
  if msg == '':
    s_msg = await ctx.send(embed=discord.Embed(title=None,description= "삭제할 메세지의 갯수를 입력해주세요", colour=0x7289da))

    await s_msg.delete(delay=3)

  # msg에 숫자값이 입력됬을경우
  elif int(msg) > 0:
  #<class 'int'> -> int 타입을 뜻하는 구절
    s_msg = await ctx.send(embed=discord.Embed(title=None,description=
    "3초뒤 "+ str(msg) + "개의 메세지 삭제됩니다.", colour=0x7289da))

    await s_msg.delete(delay=3)

    await asyncio.sleep(3)

    che = await del_message(int(msg),info_user)


  #그 외의 경우
  else:
    s_msg = await ctx.send(embed=discord.Embed(title=None,description= "잘못된 값이 입력되었습니다.", colour=0x7289da))

    await s_msg.delete(delay=3)

  
  
  if che == True:
    await asyncio.sleep(msg)

    s_msg = await ctx.send(embed=discord.Embed(title=None,description=
    "메세지가 삭제되었습니다.", colour=0x7289da))

    await s_msg.delete(delay=3)
# 기능 구현 및 예외처리 완료

client.run(TOKEN)




