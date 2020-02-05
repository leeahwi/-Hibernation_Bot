import discord
import asyncio
import aiohttp
import io


class get_images:

  def __init__(self,client,message):#기본 정보 세팅
    self.client = client
    self.ctx = message.channel
    self.user = message.author
    self.message = message

  custom_images_dict = {
    "울지참":"https://cdn.discordapp.com/attachments/646877332187119616/665544158773248021/IMG_20200111_093841.jpg",
    "오르카":"https://cdn.discordapp.com/attachments/646154916288790541/674192386703753216/95ce8ba75d0986dd.jpg",
    "제이":"https://cdn.discordapp.com/attachments/646154916288790541/674201337210077194/j.jpg",
    "냥이":"https://cdn.ppomppu.co.kr/zboard/data3/2019/0910/m_20190910001740_upyzieih.jpeg",
    }

  async def get_custom_image(self,message):
    
    for key, value in self.custom_images_dict.items():
      if key == message:

        file_url = value

        async with aiohttp.ClientSession() as session:
          async with session.get(file_url) as resp:

            if resp.status != 200:
              return await self.ctx.send('Could not download file...')

            data = io.BytesIO(await resp.read())

        await self.ctx.send(file=discord.File(data, 'image.jpg'))

      else:
        pass

