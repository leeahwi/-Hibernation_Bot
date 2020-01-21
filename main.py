import discord
import asyncio
import os
import aiohttp
import io
import random
import re

import requests
import numpy as np
import pandas as pd
import json
import datetime as dt
from bs4 import BeautifulSoup
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

###봇 기본 기능 

#클래스 변수설정
bot = bot(client)

@client.command()
async def test(message):
  
  #기본 변수
  info_user = message.author

  ctx = message.channel

  await ctx.send("testing")

#메세지 단일 또는 다중 삭제
@client.command()
async def delete(message):
  await bot.del_messages(message)

@client.command()
async def status(message):
  await bot.set_status(message)

###fun 기능

#클래스 변수설정
us_chat = userchat(client)

@client.command()
async def 꼬리(message):
  await us_chat.tale(message)

@client.command()
async def 하영(message):
  await us_chat.hayong(message)



###사이퍼즈 관련 기능

@client.command()
async def 팀배정(message):
  await divide_team(message)

@client.command()
async def 전적(message):
  await search_cypdata(message,cyp_TOKEN)

client.run(TOKEN)




