import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def bundle(ctx):

    await ctx.reply("📬 Check your DMs!")

    valid_channels = [
        c for c in ctx.guild.text_channels
        if c.permissions_for(ctx.guild.me).read_message_history
    ]

    random.shuffle(valid_channels)

    for channel in valid_channels:

        attachments = []

        async for msg in channel.history(limit=5000):
            if msg.attachments:
                for a in msg.attachments:
                    attachments.append((msg, a))

        if attachments:
            msg, file = random.choice(attachments)

            await ctx.author.send(
                content=f"📂 From {channel.mention}\n🔗 {msg.jump_url}",
                file=await file.to_file()
            )
            return

    await ctx.author.send("❌ No attachments found in any channel.")
