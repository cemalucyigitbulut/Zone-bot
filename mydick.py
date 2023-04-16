import discord
import logging
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='$yardım'))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$lan'):
        await message.channel.send('Hello!')

    if message.content.startswith('$gellan'):
        # join the voice channel the user is currently in
        if message.author.voice:
            channel = message.author.voice.channel
            await channel.connect()
        else:
            await message.channel.send("You're not in a voice channel.")

    elif message.content.startswith('$gaybol'):
        # leave the voice channel the bot is currently in
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                await vc.disconnect()
                break

    elif message.content.startswith('$yardım'):
        # display a help message
        help_message = '''
        `$gellan` - kanala gelir
        `$gaybol` - kanaldan gider
        `$yardım` - yardım gösterir
        '''
        await message.channel.send(help_message)

client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
