#기본적인 봇의 기능들 추가
#메세지 삭제, 봇 상태 설정, 기타 기능

import discord
import asyncio

class bot:
  def __init__(self, client):
    
    self.client = client

  #메세지 단일 또는 다중 삭제
  async def del_messages(self,msg):
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
      await asyncio.sleep(int(msg))

      s_msg = await ctx.send(embed=discord.Embed(title=None,description=
      "메세지가 삭제되었습니다.", colour=0x7289da))

      await s_msg.delete(delay=3)
  # 기능 구현 및 예외처리 완료

  #봇 상태 바꾸기
  #추후에 권한 설정 해야함 다른 서버에서 바꾼 내용이 적용됨
  async def set_status(self,msg):

    ctx = msg.channel

    msg = msg.message.content[8:]

    await self.client.change_presence(activity=discord.Game(name=msg))

    s_msg = await ctx.send(embed = discord.Embed(title = None, description = "상태 바꿨어요!", colour=0x7289da))

    await s_msg.delete(delay=3)
    #check it work
