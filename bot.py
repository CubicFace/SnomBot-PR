import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
from webserver import keep_alive
import os


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
        embed.add_field(name="Command", value=f".s {command}: {command.brief}", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    """
    Ask the ping, and the Snom will pong! (in ms)
    No arguments required.
    """
    await ctx.send(f'The snom has Pong! ({client.latency * 1000}ms)')

@client.command()
async def hi(ctx):
  """
  Say 'Hi' to the Snom.
  No arguments required.
  """
  sentences=['OwO','UwU',":3","^_^",'*Hiii!*']
  await ctx.send(random.choice(sentences))

@client.command(name="stop")
async def stop_bot(ctx):
    """
    This completely stop the bot.
    No argument required but being the developer is required :)
    """
    if ctx.message.author.id == 332082083604463616:
        await ctx.send("The Snom is going to sleep.")
        await client.close()






keep_alive()
client.run('NjU2OTM3NTU3MDk0ODI2MDE0.Xf4weA.lAuSJ0d_I25zwQQceYWljztubY4')