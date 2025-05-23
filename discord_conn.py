import os
import requests
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents().default()
intents.message_content = True
intents.voice_states = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='aki ', intents=intents)



@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.event
async def on_ready():
    try:
        
        for guild in bot.guilds:
            if guild.name == GUILD:
                break
        print(
            f'{client.user} se ha conectado a la siguiente guild/server:\n'
            f'{guild.name}( id: {guild.id})\n'
        )
        
        members_info = '\n - '.join([f'{member.id}: {member.nick if member.nick else member.name}' for member in guild.members]) 
        print(f'Guild members:\n - {members_info}')
        
    except Exception as e:
        print(f'Error: ', e)
        
    for guild in bot.guilds:
        for channel in guild.text_channels :
            if str(channel) == "general" :
                await channel.send('Bot Activated..')
                #await channel.send(file=discord.File('bot_join.gif'))
        print('Active in {}\n Member Count : {}'.format(guild.name, guild.member_count))

