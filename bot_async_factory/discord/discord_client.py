
import discord
import asyncio
import os
import json
import discord
from discord.ext import commands
from typing import List, Dict
from dotenv import load_dotenv

from abc_handler.abc_async_transport import AbstractConnectorAsync
from abc_handler.handlers import HiHandler, EchoHandler

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')


class DiscordBot(AbstractConnectorAsync):
    def __init__(self):
        super().__init__()
        # important to register_handler before application
        self.register_handler(HiHandler())
        self.register_handler(EchoHandler())
        # create instance for transport
        self.abc_transport = AbstractConnectorAsync()
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.bot = commands.Bot(command_prefix='!', intents=self.intents)

        @self.bot.event
        async def on_ready():
            print(f'Logged in as {self.bot.user.name}')
            # important to run it here
            await self.run()

        @self.bot.event
        async def on_message(message):
            # Avoid responding to self
            if message.author == self.bot.user:
                return

            print(f'Message from Discord {message}')
            if isinstance(message.channel, discord.DMChannel):
                # This is a direct message
                print("This is a private message!")
                source_type = 'private'
            elif isinstance(message.channel, discord.TextChannel):
                # This is a message in a server text channel
                print("This is a message in a server channel!")
                source_type = 'server'

            data = {
                'channel_id': message.channel.id,
                'author_id': message.author.id,
                'content': message.content,
                'source': 'discord',
                'source_type': source_type
            }
            await self.abc_transport.push_message(data)
            print(f'Message sent to Redis discord')


    async def get_message(self, response: Dict):
        """Pick up after logic job ready message to send back as a response to the chat."""
        print(f"Success pick up message {response}")
        # Send message by Discord client
        channel_id = response.get('channel_id')
        user_id = response.get('author_id')
        message = response.get('content')
        source_type = response.get('source_type', 'server')  # default to 'server' if not specified
        
        if source_type == 'private':
            await self.send_dm(user_id, channel_id, message)
        else:
            await self.send_to_discord(channel_id, message)

    async def send_to_discord(self, channel_id, message):
        if isinstance(channel_id, int):
            channel_id = int(channel_id)
        channel = await self.bot.fetch_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            print(f"Channel with ID {channel_id} not found.")

    async def send_dm(self, user_id, channel_id, message):
        if isinstance(user_id, int):
            user = await self.bot.fetch_channel(channel_id)
            await user.send(message)
        else:
            print(f"User with ID {user_id} not found.")

    async def bootstrap(self) -> None:
        """Set up the application."""   
       
        await self.bot.start(discord_token)     

    async def start_task(self):
        """core"""
        await self.bootstrap()       

if __name__ == "__main__":
    bot = DiscordBot()
    asyncio.run(bot.start_task())

    