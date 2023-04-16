import discord
import logging
import os
from dotenv import load_dotenv
from discord.utils import get
from pathlib import Path

load_dotenv()

TOKEN = os.getenv('TOKEN')

handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)

played_sounds = []

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='/yardım'))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/lan'):
        await message.channel.send('Hello!')

    if message.content.startswith('/gellan'):
        if message.author.voice:
            channel = message.author.voice.channel
            await message.channel.send('geldim lan geldim')
            vc = await channel.connect()
            if vc not in played_sounds:
                sound_path = Path('sounds/Zone.mp3')
                if sound_path.exists():
                    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source='sounds/Zone.mp3', executable='C:/ffmpeg/bin/ffmpeg.exe'))
                    vc.play(source)
                    played_sounds.append(vc)
            

    elif message.content.startswith('/gaybol'):
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                await vc.disconnect()
                played_sounds.remove(vc)
                await message.channel.send('bay bay lan')
                break

    elif message.content.startswith('/yardım'):
        # display a help message
        help_message = '''
        `/gellan` - kanala gelörem
        `/gaybol` - kanaldan gidörem
        `/yardım` - yardım gösterörem 
        `/gonuş` - çenıldaysa cumzonu bidaha söyler
        '''
        await message.channel.send(help_message)

    elif message.content.startswith('/gonuş'):
        # play the sound if the bot is already in a voice channel
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                sound_path = Path('sounds/Zone.mp3')
                if sound_path.exists():
                    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=str(sound_path)))
                    vc.play(source)
                    played_sounds.append(vc)
                    break
        else:
            await message.channel.send("odada deyilim lan mal")

client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
