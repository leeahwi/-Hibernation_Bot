#이미지 가져오기 함수

'''
  if message.content.startswith(COMMANDPREFIX+'울지참'):
    if message.content[3:] == '':
      async with aiohttp.ClientSession() as session:
        async with session.get('https://cdn.discordapp.com/attachments/646877332187119616/665544158773248021/IMG_20200111_093841.jpg') as resp:
          if resp.status != 200:
            return await ctx.send('Could not download file...')
        data = io.BytesIO(await resp.read())
        await ctx.send(file=discord.File(data, 'crying_hell.jpg'))    
    
  if message.content.startswith(COMMANDPREFIX+'냥냥'):
    if message.content[3:] == '':
      async with aiohttp.ClientSession() as session:
        async with session.get('https://source.unsplash.com/1600x900/?cat') as resp:
          if resp.status != 200:
            return await ctx.send('Could not download file...')
        data = io.BytesIO(await resp.read())
        await ctx.send(file=discord.File(data, 'cute_cat.jpg'))

  if message.content.startswith(COMMANDPREFIX+'멍멍'):
    if message.content[3:] == '':
      async with aiohttp.ClientSession() as session:
        async with session.get('https://source.unsplash.com/1600x900/?dog') as resp:
          if resp.status != 200:
            return await ctx.send('Could not download file...')
        data = io.BytesIO(await resp.read())
        await ctx.send(file=discord.File(data, 'cute_dog.jpg'))

  if message.content.startswith(COMMANDPREFIX+'검색'):
    if message.content[3:] == '':
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

      print(resp)
'''
