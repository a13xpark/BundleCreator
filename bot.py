import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def bundle(ctx):

    channels = [c for c in ctx.guild.text_channels if c.permissions_for(ctx.guild.me).read_messages]

    random_channel = random.choice(channels)

    attachments = []

    async for msg in random_channel.history(limit=1000):
        if msg.attachments:
            attachments.extend(msg.attachments)

    if not attachments:
        await ctx.send("No attachments found.")
        return

    file = random.choice(attachments)

    await ctx.author.send(f"From #{random_channel.name}\n{file.url}")

bot.run(TOKEN)
