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
    print(f"✅ Logged in as {bot.user}")


@bot.command()
async def bundle(ctx):

    await ctx.reply("📬 Check your DMs!")

    channels = [
        c for c in ctx.guild.text_channels
        if c.permissions_for(ctx.guild.me).read_message_history
    ]

    random_channel = random.choice(channels)

    attachments = []

    async for msg in random_channel.history(limit=2000):

        if msg.attachments:
            for file in msg.attachments:
                attachments.append((msg, file))

    if not attachments:
        await ctx.author.send("❌ No files found in that channel. Try again.")
        return

    msg, attachment = random.choice(attachments)

    try:
        await ctx.author.send(
            content=(
                f"📂 **Channel:** {random_channel.mention}\n"
                f"👤 **Uploaded by:** {msg.author}\n"
                f"🔗 **Jump to message:** {msg.jump_url}"
            ),
            file=await attachment.to_file()
        )
    except discord.Forbidden:
        await ctx.reply("❌ I can't DM you. Enable DMs from server members.")


bot.run(TOKEN)
