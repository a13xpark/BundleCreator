import discord
from discord.ext import commands
import random
import os
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def bundle(ctx):
    await ctx.reply("check ur dms g")

    # Get all text channels where the bot can read messages
    channels = [
        c for c in ctx.guild.text_channels
        if c.permissions_for(ctx.guild.me).read_message_history
    ]

    if not channels:
        await ctx.author.send("❌ No accessible channels found.")
        return

    random_channel = random.choice(channels)

    attachments = []

    async for msg in random_channel.history(limit=2000):
        if msg.attachments:
            for file in msg.attachments:
                attachments.append(file)

    if not attachments:
        await ctx.author.send("❌ No files found in that channel. Try again.")
        return

    # Send all attachments to the user
    for attachment in attachments:
        try:
            await ctx.author.send(attachment.url)
            await asyncio.sleep(1)  # Optional: prevent spam rate limits
        except discord.HTTPException:
            await ctx.reply("⚠️ Discord blocked the DM temporarily.")
        except discord.Forbidden:
            await ctx.reply("❌ I can't DM you. Enable DMs from server members.")
            break  # Stop if we can't DM the user

bot.run(TOKEN)
