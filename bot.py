import discord
from mcstatus import JavaServer
import datetime
from system import *
from json import load, loads
from pathlib import Path
import asyncio
from discord.ext import tasks
import random
import os

bot = discord.Bot(itents=discord.Intents.all())
# with open("./config.json") as f: config = load(f)
TOKEN = loads(Path("config.json").read_text())["TOKEN"]
URL = loads(Path("config.json").read_text())["URL"]
OWNER = loads(Path("config.json").read_text())["whitelist"]
INVITE = loads(Path("config.json").read_text())["INVITE"]
developer = loads(Path("config.json").read_text())["developer"]

bot.used = []
bot.owner = OWNER

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    presence.start()

@tasks.loop(seconds=5)
async def presence():
    stetements=[
        "by" + " " +developer,
        bot.status,
        bot.user.name,
    ]
    if bot.used:
        await bot.change_presence(activity=discord.Game(name=bot.used.pop(0)))
    else:
        await bot.change_presence(activity=discord.Game(name=f"{random.choice(stetements)}"))

@bot.user_command()
async def hello(ctx,user):
    await ctx.respond(f"Hello {user.mention}")

@bot.slash_command()
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author.mention}")

@bot.slash_command(description="Get minecraft server status")
async def mcstatus(ctx, ip):
    server = JavaServer.lookup(ip)
    status = server.status()
    debug = server.DEFAULT_PORT
    status.latency = int (status.latency)
    embed = discord.Embed(title=f"**Minecraft Server status**", color=0xEDE9B6,timestamp = datetime.datetime.now())
    embed.set_author(
        name=f"{ip}",
        icon_url=f"https://api.mcsrvstat.us/icon/{ip}"
    )
    embed.add_field(name="Version", value=f"```yml\n{status.version.name}```", inline=True)
    embed.add_field(name="Latency", value=f"```yml\n{zapcollor(status.latency)} | {status.latency} ms```", inline=True)
    embed.add_field(name="Players", value=f"```yml\n{status.players.online}/{status.players.max}```", inline=True)
    embed.add_field(name="Port", value=f"```yml\n{debug}```", inline=True)
    embed.add_field(name="Favicon", value=f"```yml\n{favicon(status.favicon)}```", inline=True)
    embed.add_field(name="Protocol", value=f"```yml\n{status.version.protocol}```", inline=True)
    embed.add_field(name="MOTD", value=f"```yml\n{status.description}```", inline=False)
    time = datetime.datetime.now()
    embed.set_footer(text=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar}")
    await ctx.respond(embed=embed)
    

@bot.slash_command(description="Get bot latency")
async def ping(ctx):
    embed = discord.Embed(title = "Pong!")
    embed.add_field(name = "Latency", value = f"```yml\n {zapcollor(bot.latency*1000)} | {bot.latency*1000:.0f} ms```", inline = False)
    # embed.value = f"```yml\n {zapcollor(bot.latency*1000)} | {bot.latency*1000:.0f} ms```"
    embed.color = 0xEDE9B6
    embed.set_footer(text=f"Used by {ctx.author.name}", icon_url=f"{ctx.author.avatar}")
    await ctx.respond(embed = embed)

@bot.slash_command(description="Restart bot")
async def restart(ctx):
    if ctx.author.id == bot.owner:
        await ctx.respond("Restarting...", delete_after=1)
        os.system("python bot.py")
        await bot.close()
    else:
        embed = discord.Embed()
        embed.set_author(
            name="You don't have permission!",
            icon_url=URL
        )
        embed.color = 0xdf0000
        await ctx.respond(embed=embed)

@bot.slash_command(description="invite this bot")
async def invite(ctx):
    embed = discord.Embed(title = None, description=f"[**Invite me!**]({INVITE})")
    embed.color = 0xEDE9B6
    embed.set_footer(text = f"{bot.user.name} by {developer}", icon_url=bot.user.avatar)
    await ctx.respond(embed=embed)


bot.run(TOKEN)