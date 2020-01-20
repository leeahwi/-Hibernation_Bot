#기본적인 봇의 기능들 추가
#메세지 삭제, 봇 상태 설정, 기타 기능

import discord
import asyncio


'''
  #봇 상태 바꾸기(추후에 온오프라인, 다른 용무중도 바꿀예정)
  if message.content.startswith(COMMANDPREFIX+'status'):
    msg = message.content[8:]
    await client.change_presence(activity=discord.Game(name=msg))
    await ctx.send("done")
    #check it work
'''
