import discord
import asyncio
import os
from discord import opus


from discord.ext import commands
from settings import *

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

 #메세지 단일 또는 다중 삭제, 다른사람꺼 삭제는 어케하누...
  #지금은 따로 조건 안걸었지만 나중가서는 조건 달아서 유저에 따라 메세지 삭제되게끔 할 예정
  if message.content.startswith(COMMANDPREFIX+'delete'):

      if message.content[8:] == '':
        number = 2
      #$delete 만 했을경우
      else:
        number = int(message.content[8:])
      #몇개의 메세지 삭제할건지의 변수

      
      msg = await ctx.history(limit=number+1).flatten()
      #ctx.history().flatten list 화
      
      await ctx.delete_messages(msg)
      #정상적으로 입력했을경우

      message = await ctx.send("delete checking")
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
  
client.run(TOKEN)
