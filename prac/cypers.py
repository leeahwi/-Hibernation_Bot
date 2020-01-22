import discord
import asyncio
import random
import aiohttp
from multiprocessing import Process

import os 
import time as tm
import requests
import numpy as np
import pandas as pd
import json
import datetime as dt
 
from pytz import timezone
from collections import Counter
 
 
##사퍼 사다리 기능
async def divide_team(message):

    voice = message.author.voice.channel
    ctx = message.channel

    mlist = voice.members[:]
    
    counter = 0
    #10명 채우기 위한 변수

    mlist_name=[]
    
    for i in range(0,10):
      mlist_name.append("None")
    
    #print(mlist)
    #voicechannel에 들어가 있는 사람의 이름만 mlist_name 리스트에 복사
    for i in mlist:
    
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


## 사이퍼즈 전적 검색
async def search_cypdata(message,cyp_TOKEN,client):
      ctx = message.channel

      print(message.channel)

      info_user = message.author
      
      username = message.message.content[4:]
      
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

      #예외처리 및 예외시 에러코드
      except Exception as ex:
        embed.add_field(name="에러: ", value= ex)
        embed.add_field(name="문의: ", value= "코드와 함께 dm으로 보내주세요")

      #매칭 기록 조회

      #시간 설정
      now = dt.datetime.now(timezone('Asia/Seoul'))
      now_time = dt.datetime.strftime(now, "%Y-%m-%d %H:%M")
      past = now - dt.timedelta(days=90)
      past_time = dt.datetime.strftime(past, "%Y-%m-%d %H:%M")      

      #플레이어 '매칭 기록' 조회 url
      print(playerid)
      #오타는 항상 조심합시다..
      url = "https://api.neople.co.kr/cy/players/" + playerid + "/matches?gameTypeId=normal&startDate=" + str(past_time) + "&endDate=" + str(now_time) + "&limit=100&apikey=" + cyp_TOKEN


      #matchid 정보 기록
      '''
        "rows" : [ 
          {
          "date" : "datetime.datetime",
          "matchId" : "matchId",
          "map" : {"mapId" : 201, "name" : "아인트호벤"},
          "playInfo" : {
            "result" : "win or lose",
            "random" : true or false,
            "partyUserCount" : 파티유저수,
            "characterId" : "한 사이퍼 고유 ID",
            "characterName" : "사이퍼 이름",
            "level" : 레벨, 
            "killCount" : 킬수,
            "deathCount" : 데스수,
            "assistCount" : 어시스트수,
            "attackPoint" : 공격량,
            "damagePoint" : 피해량,
            "battlePoint" : 전투점수,
            "sightPoint" : 시야점수,
            "playTime" : (숫자)/60 해야 분단위
          }
      }
      '''

      dict3 = requests.get(url).json()

      #각 요소 리스트

      #캐릭 리스트
      cha_list = []

      try:
        for i in range(0, 100):
          cha_list.append(dict3['matches']['rows'][i]['playInfo']['characterName'])
          #에러 이유 값이 제대로 불러오지 못했었음 'SEARCH_TIME_ERROR'

      except IndexError:
        pass

      if not cha_list:
        ctx.send(embed=discord.Embed(title= None, 
        description = "전적이 존재하지 않습니다."))

      cha_list = Counter(cha_list)
      #most 캐릭
      most_cha = cha_list.most_common(1)[0][0]

      #파티원 리스트
      party_count = []
      
      try:
        for i in range(0, 100):
          count = dict3['matches']['rows'][i]['playInfo']['partyUserCount']
          party_count.append(count)

      except IndexError:
        pass

      #모스트 파티원 수
      most_party = Counter(party_count).most_common(1)

      #시간대 리스트
      time_count = []
      
      try:
        for i in range(0, 100):
          time = dict3['matches']['rows'][i]['date'][11:13]
          #hour 시간 값만 가져옴
          time_count.append(time)

      except IndexError:
        pass
  
      #선호 시간대
      most_time = Counter(time_count).most_common(1)

      #매치id 리스트 50판 기준으로 두개로 나눔
      matchid_list = []

      try:
        for i in range(0, 50):
          count = dict3['matches']['rows'][i]['matchId']
          matchid_list.append(count)

      except IndexError:
        pass

      matchid_list2 = []

      try:
        for i in range(50, 100):
          count = dict3['matches']['rows'][i]['matchId']
          matchid_list2.append(count)

      except IndexError:
        pass
        

      #모스트 정보 embed 셋팅
      def set_mostfield(most):  
        #첫번째 줄
        embed.add_field(name="모스트 캐릭: "  ,value = str(most[0]))
        if str(most[1][0][0]) == '0':
          embed.add_field(name="선호 스타일",value = "솔로 플레이어")
        else:  
          embed.add_field(name="선호 스타일: ",value = str(most[1][0][0]) + "명 파티")
        embed.add_field(name="선호 시간대: ",value = str(most[2][0][0])+ ", " + str(most[2][0][1]) + "시")
      
      #90일간 전적중 100게임 가장 많이 한 캐릭터
      most = []
      most = [most_cha,most_party,most_time]
      #most[0] = 모스트 캐릭
      #most[1] = 모스트 파티원
      #most[2] = 모스트 시간대

      #모스트 목록 세팅
      set_mostfield(most)

      await ctx.send(embed=embed)

      
      #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
      ## 사이퍼즈 전적 검색
async def test_search_cypdata(message,cyp_TOKEN,client):
      ctx = message.channel

      print(message.channel)

      info_user = message.author
      
      username = message.message.content[4:]
      
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

      #예외처리 및 예외시 에러코드
      except Exception as ex:
        embed.add_field(name="에러: ", value= ex)
        embed.add_field(name="문의: ", value= "코드와 함께 dm으로 보내주세요")

      #매칭 기록 조회

      #시간 설정
      now = dt.datetime.now(timezone('Asia/Seoul'))
      now_time = dt.datetime.strftime(now, "%Y-%m-%d %H:%M")
      past = now - dt.timedelta(days=90)
      past_time = dt.datetime.strftime(past, "%Y-%m-%d %H:%M")      

      #플레이어 '매칭 기록' 조회 url
      print(playerid)
      #오타는 항상 조심합시다..
      url = "https://api.neople.co.kr/cy/players/" + playerid + "/matches?gameTypeId=normal&startDate=" + str(past_time) + "&endDate=" + str(now_time) + "&limit=100&apikey=" + cyp_TOKEN


      #matchid 정보 기록
      '''
        "rows" : [ 
          {
          "date" : "datetime.datetime",
          "matchId" : "matchId",
          "map" : {"mapId" : 201, "name" : "아인트호벤"},
          "playInfo" : {
            "result" : "win or lose",
            "random" : true or false,
            "partyUserCount" : 파티유저수,
            "characterId" : "한 사이퍼 고유 ID",
            "characterName" : "사이퍼 이름",
            "level" : 레벨, 
            "killCount" : 킬수,
            "deathCount" : 데스수,
            "assistCount" : 어시스트수,
            "attackPoint" : 공격량,
            "damagePoint" : 피해량,
            "battlePoint" : 전투점수,
            "sightPoint" : 시야점수,
            "playTime" : (숫자)/60 해야 분단위
          }
      }
      '''

      dict3 = requests.get(url).json()

      #각 요소 리스트

      #캐릭 리스트
      cha_list = []

      try:
        for i in range(0, 100):
          cha_list.append(dict3['matches']['rows'][i]['playInfo']['characterName'])
          #에러 이유 값이 제대로 불러오지 못했었음 'SEARCH_TIME_ERROR'

      except IndexError:
        pass

      if not cha_list:
        ctx.send(embed=discord.Embed(title= None, 
        description = "전적이 존재하지 않습니다."))

      cha_list = Counter(cha_list)
      #most 캐릭
      most_cha = cha_list.most_common(1)[0][0]

      #파티원 리스트
      party_count = []
      
      try:
        for i in range(0, 100):
          count = dict3['matches']['rows'][i]['playInfo']['partyUserCount']
          party_count.append(count)

      except IndexError:
        pass

      #모스트 파티원 수
      most_party = Counter(party_count).most_common(1)

      #시간대 리스트
      time_count = []
      
      try:
        for i in range(0, 100):
          time = dict3['matches']['rows'][i]['date'][11:13]
          #hour 시간 값만 가져옴
          time_count.append(time)

      except IndexError:
        pass
  
      #선호 시간대
      most_time = Counter(time_count).most_common(1)

      #매치id 리스트 50판 기준으로 두개로 나눔
      matchid_list = []

      try:
        for i in range(0, 50):
          count = dict3['matches']['rows'][i]['matchId']
          matchid_list.append(count)

      except IndexError:
        pass

      matchid_list2 = []

      try:
        for i in range(50, 100):
          count = dict3['matches']['rows'][i]['matchId']
          matchid_list2.append(count)

      except IndexError:
        pass
        

      #모스트 정보 embed 셋팅
      def set_mostfield(most):  
        #첫번째 줄
        embed.add_field(name="모스트 캐릭: "  ,value = str(most[0]))
        if str(most[1][0][0]) == '0':
          embed.add_field(name="선호 스타일",value = "솔로 플레이어")
        else:  
          embed.add_field(name="선호 스타일: ",value = str(most[1][0][0]) + "명 파티")
        embed.add_field(name="선호 시간대: ",value = str(most[2][0][0])+ ", " + str(most[2][0][1]) + "시")
      
      #90일간 전적중 100게임 가장 많이 한 캐릭터
      most = []
      most = [most_cha,most_party,most_time]
      #most[0] = 모스트 캐릭
      #most[1] = 모스트 파티원
      #most[2] = 모스트 시간대

      #모스트 목록 세팅
      set_mostfield(most)

      await ctx.send(embed=embed)
