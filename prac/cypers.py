import discord
import asyncio
import random
import aiohttp
from discord.ext import commands


import os 
import time as tm
import requests
import numpy as np
import pandas as pd
import json
import datetime as dt
 
from pytz import timezone
from collections import Counter

class cypers_searcher:
  block ='''
```유저 이름: {}

클랜: {}
티어: {}

일반 승률: {}%
승: {}, 패: {}, 탈주: {}

공식 승률: {}%
승: {}, 패: {}, 탈주: {}
```'''

  
  def __init__(self,client,cyp_TOKEN,message):#클래스 변수 세팅
    self.client = client
    self.cyp_TOKEN = cyp_TOKEN
    self.ctx = message.channel
    self.user = message.author
    self.message = message

    self.limit = 200  #매치 id limit 

    self.cypers_user_name = ''

  async def get_info(self,message):#기본 정보 가져오기
    '''
    parameter = 'message'

    returns:
      player_info_data:
        playerId,
        nickname,
        grade,
    '''
    msg = message.message.content
    
    search_name = msg[4:]

    print(search_name)

    try:

      url = "https://api.neople.co.kr/cy/players?nickname=" + search_name + "&wordType=match&apikey=" + self.cyp_TOKEN

      dict = requests.get(url).json()

      playerId = dict['rows'][0]['playerId']#유저 고유 아이디
      nickname = dict['rows'][0]['nickname']#유저 닉네임
      grade = dict['rows'][0]['grade']#유저 급수

      self.cypers_user_name = nickname #뒤에 포지션 끌어오기에서 쓸 예정

      player_info_data = {'playerid':playerId,
                          'nickname':nickname,
                          'grade':grade}

      return  player_info_data #기본 정보 반환

    except IndexError:
        msg = await self.ctx.send(embed=discord.Embed(title=None,description= "검색할 유저의 닉네임을 입력해주세요"))
        await msg.delete(delay=3)
        return IndexError

    except requests.exceptions.RequestException:
      await self.ctx.send(embed=discord.Embed(title="서버가 응답하지 않습니다."))
      await msg.delete(delay=3)

  async def get_vict(self,playerId):#승리,패배,탈주 정보 가져오기

    url = "https://api.neople.co.kr/cy/players/" + playerId + "?apikey=" + self.cyp_TOKEN
  
    dict = requests.get(url).json()
  
    #1. 공식과 일반 둘다 존재하는 경우
    #2. 일반만 존재 하는 경우(공식 조건 안되는 경우가 이에 해당함)
    #3. 둘다 존재 안하는 경우(협력만 돌렸거나, 랭크가 1인경우가 이에 해당함)
    
    print(dict)
    #공식 매치 결과 기본값
    rank_wincount = 0
    rank_lostcount = 0
    rank_stopcount = 0

    #일반 매치 결과 기본값
    normal_wincount = 0
    normal_losecount = 0
    normal_stopcount = 0

    if dict['records'] == []:
      discord_message = await self.ctx.send(embed=discord.Embed(title=None,description= "일반, 공식 기록이 없습니다."))
      await discord_message.delete(delay=3)

    #일반전
    elif dict['records'][0]['gameTypeId'] == 'normal':
      normal_wincount = dict['records'][1]['winCount']
      normal_losecount = dict['records'][1]['loseCount']
      normal_stopcount = dict['records'][1]['stopCount']

    #공식전
    else:
      #공식 기록
      rank_wincount = dict['records'][0]['winCount']
      rank_lostcount = dict['records'][0]['loseCount']
      rank_stopcount = dict['records'][0]['stopCount']
      #일반 기록
      normal_wincount = dict['records'][1]['winCount']
      normal_losecount = dict['records'][1]['loseCount']
      normal_stopcount = dict['records'][1]['stopCount']


    play_count_dict = {
    "normal": [normal_wincount,normal_losecount,normal_stopcount],
    "rank":[rank_wincount,rank_lostcount,rank_stopcount],
    "clantier":[dict['clanName'],dict['tierName']]
    }

    return play_count_dict
  
  async def get_match(self,playerId):#매치 정보 가져오기
    ''' 
      returns:
        dict
    '''
    #시간 설정
    now = dt.datetime.now(timezone('Asia/Seoul'))
    now_time = dt.datetime.strftime(now, "%Y-%m-%d %H:%M")
    past = now - dt.timedelta(days=30)
    past_time = dt.datetime.strftime(past, "%Y-%m-%d %H:%M")      

    try:
      url = "https://api.neople.co.kr/cy/players/" + str(playerId) + "/matches?gameTypeId=normal&startDate=" + str(past_time) + "&endDate=" + str(now_time) + "&limit=" + str(self.limit) + "&apikey=" + self.cyp_TOKEN #30일 기준 최대 200판 까지

      dict = requests.get(url).json()

      #print(dict,sep = '\n')

      return dict

    except requests.exceptions.RequestException:
          msg = await self.ctx.send(embed=discord.Embed(title="서버가 응답하지 않습니다."))
          await msg.delete(delay=3)
    
    except Exception as ex:
      print(ex)

  def get_character(self,dict, limit = 200): #각 매치의 유저의 플레이한 캐릭터 가져오기, 제한판수 입력 없을시 self.limit 값 들어감
    '''
      returns:
        character_name_list
    '''
    character_name_list = []

    try:
      for i in range(0, limit):
        count = dict['matches']['rows'][i]['playInfo']['characterName']
        if count == "":
          pass
        else:
          character_name_list.append(count)
      return character_name_list
        
    except IndexError:#아무것도 없을 경우 
      pass

    if not character_name_list:
      return False

  def get_party_list(self,dict): #각 매치 판의 파티원 수 가져오기
    party_count_list = []
    
    try:
      for i in range(0, self.limit):
        count = dict['matches']['rows'][i]['playInfo']['partyUserCount']
        party_count_list.append(count)
      
      return party_count_list

    except IndexError:
      pass

    if not party_count_list:
      return False #이 경우 솔로 플레이어로 나타나게 한다
    
  def get_start_playtime(self,dict): #각 매치의 시작한 시간 가져오기
    time_count = []
    
    try:
      for i in range(0, self.limit):
        time = dict['matches']['rows'][i]['date'][11:13]
        print(time) # 체크 해봐야함
        time_count.append(time)
      return time_count

    except IndexError:
      pass

    if not time_count:
      return False
    
  def get_matchid(self,dict): #각 매치의 고유 ID 가져오기
    matchid_list = [] 

    try:
      for i in range(0, int(self.limit)):
        matchid = dict['matches']['rows'][i]['matchId']
        matchid_list.append(matchid)
      return matchid_list

    except IndexError:
      pass  
    
    if not matchid_list:
      return False

  def get_match_result(self,dict): #각 매치 결과 가져오기

    result_list = []

    try:
      for i in range(0,self.limit):
        result = dict['matches']['rows'][i]['playInfo']['result']
        result_list.append(result)
      return result_list

    except IndexError:
      return False
    
  def get_match_kda(self,dict): #각 매치 kda, 피해량 등 가져오기
    kill_count_list = []
    death_count_list = []
    assist_count_list = []
    attack_count_list = []
    damage_count_list = []
    battle_count_list = []
    sight_count_list = []
    playtime_count_list = []

    '''
      "playInfo":
      "result" : "(win,lose)",
      "random" : (bool),
      "partyUserCount" : (int),
      "characterId" : "***",
      "characterName" : "---",
      "level" : (int),
      "killCount" : (int),
      "deathCount" : (int),
      "assistCount" : (int),
      "attackPoint" : (int),
      "damagePoint" : (int),
      "battlePoint" : (int),
      "sightPoint" : (int),
      "playTime" : (int)
    '''

    try:
      for i in range(0,self.limit):
        kill_count = dict['matches']['rows'][i]['playInfo']['killCount']
        death_count = dict['matches']['rows'][i]['playInfo']['deathCount']
        assist_count = dict['matches']['rows'][i]['playInfo']['assisCount']
        attack_count = dict['matches']['rows'][i]['playInfo']['atttackPoint']
        damage_count = dict['matches']['rows'][i]['playInfo']['damagePoint']
        battle_count = dict['matches']['rows'][i]['playInfo']['battlePoint']
        sight_count = dict['matches']['rows'][i]['playInfo']['sightPoint']
        playtime_count = dict['matches']['rows'][i]['playInfo']['playTime']

        kill_count_list.append(kill_count)
        death_count_list.append(death_count)
        assist_count_list.append(assist_count)
        attack_count_list.append(attack_count)
        damage_count_list.append(damage_count)
        battle_count_list.append(battle_count)
        sight_count_list.append(sight_count)
        playtime_count_list.append(playtime_count)


  
    except IndexError:
      return False

  async def get_position_info(self,matchid):#포지션 정보 크롤링
      async with aiohttp.ClientSession() as client:
        async with client.get('https://api.neople.co.kr/cy/matches/'+ matchid + '?&apikey=' + self.cyp_TOKEN) as resp:

          if resp.status == 400:
            print("error")
            raise IndexError
              
          if resp.status == 200:
            print("done")

          temp_dict = await resp.text()

          temp_dict = json.loads(temp_dict)
      
          try:
              for i in range(0, 10):
                  if temp_dict['players'][i]['nickname'] == self.cypers_user_name:
                      position_name = temp_dict['players'][i]['position']['name']
                  
          except IndexError:
              pass

          return position_name

  async def sync_get_position(self,matchid_list):#포지션 함수 비동기 처리
    
    coroutines = (self.get_position_info(matchid) for matchid in matchid_list)

    return await asyncio.gather(*coroutines)

  async def fetch_position_info(self,matchid_list):#포지션 리스트로 내보내기

    position_dict = {}

    for i,response in enumerate(await self.sync_get_position(matchid_list)):
    
      position_dict[i] = response

    for key, value in position_dict.items():
      print('{} : {}'.format(key,value))

    return position_dict

  def count_most_common(self,list): #가장 많이 나온 요소 가져오기
    most_list = Counter(list).most_common(1)
    return most_list

  async def send_basic_record(self,search_message): #기본 전적 discord 메세지 보내기
    player_info_data = await self.get_info(search_message)
    vict_count_dict = await self.get_vict(player_info_data['playerid'])

    try: 
      normal_countkda = vict_count_dict['normal'][0] /(vict_count_dict['normal'][0] + vict_count_dict['normal'][1]) 
      vict_normal_persent = round(normal_countkda * 100 , 2)
    except:
      vict_normal_persent = 0

    try:
      rank_countkda = vict_count_dict['rank'][0] / (vict_count_dict['rank'][0] + vict_count_dict['rank'][1])

      vict_rank_persent = round(rank_countkda * 100 , 2)
    except:
      vict_rank_persent = 0

    basic_info = self.block.format(player_info_data['nickname'],
              *vict_count_dict['clantier'],
               vict_normal_persent, *vict_count_dict['normal'],
               vict_rank_persent, *vict_count_dict['rank'])
    
    await self.ctx.send(basic_info)

  async def send_top_chars(self,search_message): #최근 50판중 most 7 캐릭터 discord 출력
    player_info_data = await self.get_info(search_message)

    dict = await self.get_match(player_info_data['playerid'])

    character_name_list = self.get_character(dict,50)

    if len(character_name_list) < 7:
      most_charlist = Counter(character_name_list).most_common(len(character_name_list))
    else:
      most_charlist = Counter(character_name_list).most_common(7)

    send_list = []
    for i, char in enumerate(most_charlist,start=1):
      send_list.append("{}. {} : {}판".format(i,char[0],char[1]))
    send_message = ""

    for list in send_list:
      send_message += list + '\n' 

    await self.ctx.send(f"```최근 50판 중 TOP 7\n{send_message}```")

