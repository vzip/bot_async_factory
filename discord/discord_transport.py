import redis
import discord

import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
redis_client = redis.Redis(host=redis_host, port=redis_port)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    data = {
        'channel_id': message.channel.id,
        'author_id': message.author.id,
        'content': message.content
    }
    redis_client.lpush('discord', json.dumps(data))
    print(f'Message sent to Redis discord')

async def send_to_discord(channel_id, message):
    channel = bot.get_channel(channel_id)
    await channel.send(message)


@bot.command()
async def send(ctx, *, message: str):
    await send_to_discord(message)

bot.run(discord_token)
