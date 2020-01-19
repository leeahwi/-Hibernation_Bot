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

from pytz import timezone
from discord import opus
from discord.ext import commands

TOKEN = os.environ['BOT_TOKEN']
cyp_TOKEN = os.environ['CYP_TOKEN']

client = discord.Client()

COMMANDPREFIX = '$'


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


  #메세지 단일 또는 다중 삭제, 다른사람꺼 삭제는 어케하누... -> 다른사람꺼는 삭제 안되게 함
  #이제 메세지 친 유저의 메세지만 삭제됨
  #봇 메세지는 시간후에 삭제되도록 함
  #추가로 특정 조건을 가진 사람들은 다른사람 메세지도 삭제 가능하게 할 기능 추가 예정
  if message.content.startswith(COMMANDPREFIX+'delete'):
      
      user = message.author

      print(message.author)

      if message.content[8:] == '':
        number = 2
      #$delete 만 했을경우
      else:
        number = int(message.content[8:]) + 1 
      #몇개의 메세지 삭제할건지의 변수
      
      message = await ctx.send(embed=discord.Embed(title="3초뒤 메세지 삭제됩니다.",type="rich",colour=0x7289da))
      await message.delete(delay=5)
      #메세지 삭제 안내 구문

      def predicate(message):
        return not message.author.bot
      #봇 메세지를 msg에 넣지 않음

      counter = 0
      #삭제할 메세지 갯수

      async for msg in ctx.history(limit=200).filter(predicate):
        if msg.author == user:
          await msg.delete(delay=3)
          counter += 1
        if counter == number:
          break
      
  #check it work
 
  #봇 상태 바꾸기(추후에 온오프라인, 다른 용무중도 바꿀예정)
  if message.content.startswith(COMMANDPREFIX+'status'):
      msg = message.content[8:]
      await client.change_presence(activity=discord.Game(name=msg))
      await ctx.send("done")
    #check it work
  
  if message.content.startswith(COMMANDPREFIX+'hello'):

    await ctx.send('hello!')

    def check_predicate(message):
        return message.content == 'hello' and message.channel == ctx

    msg = await client.wait_for('message', check = check_predicate, timeout = 100)

    await ctx.send('Hello {.author}!'.format(msg))
    await ctx.send(f'{msg} has connected to Discord!')
  #check it work

  if message.content.startswith(COMMANDPREFIX+'embed'):

    emb = discord.Embed(title="test",description="test용 embed 입니다",colour = 0x2ecc71 )

    emb.set_thumbnail(url="https://cdn.discordapp.com/avatars/260754328187305984/b144bfacf229dce0f3b912185ddd364d.png?size=128")

    emb.add_field(name="test1", value="바보들")

    emb.set_author(name='숄쯋유라',url="https://cdn.discordapp.com/avatars/260754328187305984/b144bfacf229dce0f3b912185ddd364d.png?size=128", icon_url="https://cdn.discordapp.com/avatars/260754328187305984/b144bfacf229dce0f3b912185ddd364d.png?size=128")

    emb.set_footer(icon_url=message.author.avatar_url,text='Requested by {}'.format(message.author.display_name))

    emb.set_image(url=message.author.avatar_url)

    #emoji =  client.get_emoji(658164817458102302)
    #이건 작동 안했음

    emoji = '\N{THUMBS UP SIGN}'
    #checked

    emb.add_field(name="tess",value=emoji)


    #You use the Message.add_reaction() method.
    #If you want to use unicode emoji, you must pass a valid unicode code point in a string. In your code, you can write this in a few different ways:

    #'👍'

    #'\U0001F44D'

    #'\N{THUMBS UP SIGN}'

    emb.insert_field_at(index=1,name="tes2",value=emoji,inline=True)

    emb.insert_field_at(index=1,name="tes3",value=emoji,inline=False)

    emb.set_field_at(index=1,name="tes4", value=emoji, inline=False)
    
    #imageURL = "https://cdn.discordapp.com/avatars/260754328187305984/b144bfacf229dce0f3b912185ddd364d.png?size=128"
    #embed.description("checked")
    #embed.set_image(imageURL)

    await ctx.send(embed=emb)
    
  #이미지 업로드 
  #검색기능도 만들었지만 일단 위험성이 있다고 생각해 봉인
  if message.content.startswith(COMMANDPREFIX+'울지참'):
    async with aiohttp.ClientSession() as session:
      async with session.get('https://cdn.discordapp.com/attachments/646877332187119616/665544158773248021/IMG_20200111_093841.jpg') as resp:
        if resp.status != 200:
            return await ctx.send('Could not download file...')
        data = io.BytesIO(await resp.read())
        await ctx.send(file=discord.File(data, 'crying_hell.jpg'))    
    
  if message.content.startswith(COMMANDPREFIX+'냥냥'):
    async with aiohttp.ClientSession() as session:
      async with session.get('https://source.unsplash.com/1600x900/?cat') as resp:
        if resp.status != 200:
            return await ctx.send('Could not download file...')
        data = io.BytesIO(await resp.read())
        await ctx.send(file=discord.File(data, 'cute_cat.jpg'))

  if message.content.startswith(COMMANDPREFIX+'멍멍'):
    async with aiohttp.ClientSession() as session:
      async with session.get('https://source.unsplash.com/1600x900/?dog') as resp:
        if resp.status != 200:
            return await ctx.send('Could not download file...')
        data = io.BytesIO(await resp.read())
        await ctx.send(file=discord.File(data, 'cute_dog.jpg'))
        
  if message.content.startswith(COMMANDPREFIX+'검색'):
    #if message.author.id == 260754328187305984:
    keyword = message.content[4:]
      #checking
    print(keyword)

    async with aiohttp.ClientSession() as session:
      async with session.get('https://source.unsplash.com/1600x900/?'+keyword) as resp:
        if resp.status != 200:
            return await ctx.send('Could not download file...')
        data = io.BytesIO(await resp.read())
        await ctx.send(file=discord.File(data, 'search_keyword.jpg'))
      
      
  
  if message.content.startswith(COMMANDPREFIX+'하영'):
    if message.content[3:] == '':
      #msg = message.content[3:]
      #print(msg)
      await ctx.send(embed=discord.Embed(title="아프니까...청춘이다... by.'유하영'",colour=0xe74c3c))

  if message.content.startswith(COMMANDPREFIX+'꼬리'):
    if message.content[3:] == '':
      await ctx.send(embed=discord.Embed(title="바보졸개",colour=0x7289da))
    
  if message.content.startswith(COMMANDPREFIX+'졸개'):
    if message.content[3:] == '':
      await ctx.send(embed=discord.Embed(title="바보꼬리",colour=0x7289da))
    
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
      await ctx.send(embed=discord.Embed(title="샆창",colour=0x7289da))


  if message.content.startswith(COMMANDPREFIX+'감자'):
    if message.content[3:] == '':
      await ctx.send(embed=discord.Embed(title="감자'바보'",colour=0x7289da))


  if message.content.startswith(COMMANDPREFIX+'새우'):
    if message.content[3:] == '':
      await ctx.send(embed=discord.Embed(title="막냉이",colour=0x7289da))
 
  
        
  
  ##사퍼 사다리 기능
  if message.content.startswith(COMMANDPREFIX+'팀배정'):
    if message.content[4:] == '':
      voice = message.author.voice.channel
      '''
      print(str(voice.id) + voice.name)
      print(voice.members[1].name)
      print(voice.members[1].id)
      print(voice.members[1].bot)
      print(voice.members[0].bot)
      print(voice.members[0].id)
      '''

      mlist = voice.members[:]
      

      counter = 0
      #10명 채우기 위한 변수

      mlist_name=[]
      
      for i in range(0,10):
        mlist_name.append("None")
      
      #print(mlist)
      #voicechannel에 들어가 있는 사람의 이름만 mlist_name 리스트에 복사
      for i in mlist:
        
        print(mlist[counter].bot)
      

        if counter == 10:
          break
        
        if mlist[counter].bot == False:
            mlist_name.remove("None")
            mlist_name.append(mlist[counter].display_name)
    
        counter +=1

      #print(mlist_name)
      
      random.shuffle(mlist_name)
      while abs(mlist_name[0:5].count("None")-mlist_name[5:10].count("None")) >= 2:
        random.shuffle(mlist_name)

      #랜덤으로 팀 배정
      #print(mlist_name)

      #print(mlist_name[0:5])
      #print(mlist_name[5:10])

      await ctx.send(embed=discord.Embed(title= "1팀: " + ', '.join((str(i) for i in mlist_name[0:5])),colour=0xe74c3c))

      await ctx.send(embed=discord.Embed(title= "2팀: " + ', '.join((str(i) for i in mlist_name[5:10])),colour=0x3498db))

    else:
      await message.delete(delay=None)
      #이용자 메세지 삭제
      msg = await ctx.send("'팀배정'이라 쳐야 작동되요! (｡ŏ﹏ŏ)｡ ")
      await msg.delete(delay=3)
      #봇 메세지 삭제
    
    
## 사이퍼즈 전적 검색
  if message.content.startswith(COMMANDPREFIX+'전적'):
    #if message.content[3:] == " ":

      username = message.content[4:]
      
      #print(username)
      
      try:
        url = "https://api.neople.co.kr/cy/players?nickname=" + username + "&wordType=match&apikey=" + cyp_TOKEN
        
        dict = requests.get(url).json()
        #뒤에 () 괄호 없어서 오류 뜸 ㅋ 왜그런지는 잘 모르겠네
        playerid = dict['rows'][0]['playerId']
        user = dict['rows'][0]['nickname']
        grade = dict['rows'][0]['grade']


      except IndexError:
        await message.delete(delay=0)
        msg = await ctx.send(embed=discord.Embed(title="닉네임이 존재하지 않습니다."))
        await msg.delete(delay=3)

      except requests.exceptions.RequestException:
        await message.delete(delay=0)
        await ctx.send(embed=discord.Embed(title="서버가 응답하지 않습니다."))
        await msg.delete(delay=3)

      '''
      user = nickname
      grade = 급수
      clanName = 클랜이름
      ratingpoint = 공식전 점수?
      maxRatingPoing = 최대 점수
      tierName = 공식 티어
      records 
      [
        gameTypeId = rating <- rating 으로 값일경우 공식전 데이터 라는 뜻
        winCount = 이긴횟수
        loseCount" : 진횟수,
        stopCount" : 나간횟수
      ]
       "gameTypeId" : "normal",
        "winCount" : 2097,
        "loseCount" : 1768,
        "stopCount" : 67
      '''

      #print(user)
      #print(playerid)

      #기본 embed 양식
      embed=discord.Embed(
        title = None,
        colour = 0x3498db
      )

      #기본 정보 셋팅
      def player_info():
        embed.add_field(name= "이름: ", value = user)
        embed.add_field(name= "급수: ", value = grade)
        embed.add_field(name= "\n\u200b" , value = "승패 기록"  ,inline=False)
      
      #'\u200b' -> 빈공간
      #"\n\u200b"

      player_info()
    
      try:
        url = "https://api.neople.co.kr/cy/players/" + playerid + "?apikey=" + cyp_TOKEN
        #플레이어의 정보 조회 api 주소
        dict2 = requests.get(url).json()
        #dict 형태로 정리된 정보
        #1. 공식과 일반 둘다 존재하는 경우
        #2. 일반만 존재 하는 경우(공식 조건 안되는 경우가 이에 해당함)
        #3. 둘다 존재 안하는 경우(협력만 돌렸거나, 랭크가 1인경우가 이에 해당함)
        
        #공식 매치 결과 기본값
        rw_count, rl_count, rs_count = 0,0,0
        #일반 매치 결과 기본값
        w_count, l_count, s_count = 0,0,0
        #w_count,l_count,s_count = 0 -> non-iterable int object error

        #사이퍼즈 아이콘
        embed.set_author(
          name = "사이퍼즈 전적 검색",
          url= "http://cyphers.nexon.com/cyphers/main",icon_url="https://cdn.discordapp.com/attachments/646154916288790541/668263428065984513/cypers_icon.jpg"
          )

        #승패 기록 필드 세팅
        def set_infofield():
          #첫번째 줄
          embed.add_field(name="공식 승: ",value = rw_count)
          embed.add_field(name="공식 패: ",value = rl_count)
          embed.add_field(name="공식 탈주: ",value = rs_count)
          #두번째 줄
          embed.add_field(name="일반 승: ",value = w_count)
          embed.add_field(name="일반 패: ",value = l_count)
          embed.add_field(name="일반 탈주: ",value = s_count)

        #3번 조건 일시
        if dict2['records'] == []:
          embed.add_field(name="에러: ",value="일반,공식 기록이 없는 플레이어 입니다.")

        #2번 조건 일시
        elif dict2['records'][0]['gameTypeId'] == 'normal':
          w_count = dict2['records'][0]['winCount']
          l_count = dict2['records'][0]['loseCount']
          s_count = dict2['records'][0]['stopCount']
          set_infofield()
        
        #1번 조건 일시
        else:
          #공식 기록
          rw_count = dict2['records'][0]['winCount']
          rl_count = dict2['records'][0]['loseCount']
          rs_count = dict2['records'][0]['stopCount']
          #일반 기록
          w_count = dict2['records'][1]['winCount']
          l_count = dict2['records'][1]['loseCount']
          s_count = dict2['records'][1]['stopCount']
          set_infofield()
        
        await ctx.send(embed=embed)

      #예외처리 및 예외시 에러코드
      except Exception as ex:
        embed.add_field(name="에러: ", value= ex)
        embed.add_field(name="문의: ", value= "코드와 함께 dm으로 보내주세요")

client.run(TOKEN)
