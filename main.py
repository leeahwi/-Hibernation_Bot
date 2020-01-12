import discord
import asyncio
import os
import aiohttp
import io

from discord.ext import commands

TOKEN = os.environ['BOT_TOKEN']

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
  #흠.. 명령어 다음에 오는 말에 따라 검색한 키워드 랜덤 이미지 불러올수있게 하자
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
    if message.user.id == 260754328187305984:
      keyword = message.content[4:]
      #checking
      print(keyword)

      async with aiohttp.ClientSession() as session:
        async with session.get('https://source.unsplash.com/1600x900/?'+keyword) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
        data = io.BytesIO(await resp.read())
        await ctx.send(file=discord.File(data, 'search_keyword.jpg'))

        
  
client.run(TOKEN)
