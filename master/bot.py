import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random

client = commands.Bot(command_prefix=".s ")

@client.event
async def on_ready():
    print("[INFO] On.")

@client.event
async def on_member_join(member):
    print(f'[INFO] {member} joined.')

@client.event
async def on_member_remove(member):
    print(f'[INFO] {member} left.')

@client.command()
async def ping(ctx):
    """
    Ask the ping, and the Snom will pong! (in ms)
    """
    await ctx.send(f'The snom has Pong! ({client.latency * 1000}ms)')

client.run('NjU2OTM3NTU3MDk0ODI2MDE0.Xfp7IQ.ItambosdWjmIUnWG_KtSU3qXx-A')