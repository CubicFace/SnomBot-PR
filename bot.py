import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random

client = commands.Bot(command_prefix=".s ")

client.remove_command('help')

@client.event
async def on_ready():
    print("[INFO] On.")

@client.event
async def on_member_join(member):
    print(f'[INFO] {member} joined.')

@client.event
async def on_member_remove(member):
    print(f'[INFO] {member} left.')

@client.command(name="help", description="The Snom is here to help.")
async def help(ctx, cmd=None):
    embed=discord.Embed(colour=discord.Colour(0xbfcdff), title="Help")
    for command in ctx.bot.commands:
        embed.add_field(name="Command", value=f".s {command}: {help}", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    """
    Ask the ping, and the Snom will pong! (in ms)
    No arguments required.
    """
    await ctx.send(f'The snom has Pong! ({client.latency * 1000}ms)')


@client.command(name="stop")
async def stop_bot(ctx):
    """
    This completely stop the bot.
    No argument required but being the developer is required :)
    """
    if ctx.message.author.id == 332082083604463616:
        await ctx.send("The Snom is going to sleep.")
        client.close()








client.run('NjU2OTM3NTU3MDk0ODI2MDE0.Xf1JMw.5WbBp7yozPUDo9cL2tp5YDaIglw')