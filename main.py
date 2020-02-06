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


@client.command()
async def test(message):
  await ctx.send("testing")

###봇 기본 기능 
bot = bot(client)
#메세지 단일 또는 다중 삭제
@client.command()
async def 삭제(message):
  await bot.delete_user_messages(message)
#봇 스탯 바꾸기
@client.command()
async def 상태(message):
  await bot.set_status(message)
#팀배정 하기
@client.command()
async def 팀배정(message):
  await bot.divide_team(message)

###이미지 업로드 관련 기능
@client.command()
async def 이미지(message):
  image = get_images(client,message)
  search_message = message.message.content[5:]
  task = await image.send_custom_image(search_message)
  if task != True:
    await image.send_random_image(search_message)



###사이퍼즈 관련 기능

@client.command()
async def 전적(message):
  await search_cypdata(message,cyp_TOKEN,client)

client.run(TOKEN)




