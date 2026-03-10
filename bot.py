import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def bundle(ctx):

    # tell the user to check DMs
    await ctx.reply("📬 Check your DMs!")

    channels = [
        c for c in ctx.guild.text_channels
        if c.permissions_for(ctx.guild.me).read_messages
    ]

    random_channel = random.choice(channels)

    attachments = []

    async for msg in random_channel.history(limit=1000):
        if msg.attachments:
            attachments.append((msg, msg.attachments[0]))

    if not attachments:
        await ctx.author.send("No attachments found, try again.")
        return

    msg, attachment = random.choice(attachments)

    # send the file/video directly to DM
    await ctx.author.send(
        content=f"📂 From {random_channel.mention}",
        file=await attachment.to_file()
    )

bot.run(TOKEN)
