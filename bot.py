import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import traceback
import sys
from webserver import keep_alive
import os


client = commands.Bot(command_prefix=".s ")

client.remove_command('help')

@client.event
async def on_ready():
    print("[INFO] On.")
    print(f"""
    [INFO] Bot info:
    User ID: {client.user.id}
    Name: {client.user.name}
    """)

@client.event
async def on_member_join(member):
    print(f'[INFO] {member} joined.')

@client.event
async def on_member_remove(member):
    print(f'[INFO] {member} left.')

@client.command(name="help", brief="The Snom is here to help.")
async def help(ctx, cmd=None):
    embed=discord.Embed(colour=discord.Colour(0xbfcdff), title="Help")
    for command in ctx.bot.commands:
        embed.add_field(name="Command", value=f".s {command}: {command.brief}", inline=True)
    await ctx.send(embed=embed)

@client.command(brief="Ask the ping, and the Snom will pong! (in ms)")
async def ping(ctx):
    """
    Ask the ping, and the Snom will pong! (in ms)
    No arguments required.
    """
    print(f"[INFO][COMMAND]Ping by {ctx.message.author.name}. Actual bot latency: {client.latency * 1000} ms.")
    await ctx.send(f'The snom has Pong! ({round(client.latency * 1000,2)} ms)')

@client.command(brief="Say 'Hi' to the Snom.")
async def hi(ctx):
  """
  Say 'Hi' to the Snom.
  No arguments required.
  """
  sentences=['OwO','UwU',":3","^_^",'*Hiii!*']
  chosed_sentence=random.choice(sentences)
  print(f"[INFO][COMMAND]'hi' command by {ctx.message.author.name}. Chosen sentence: '{chosed_sentence}'")
  await ctx.send(chosed_sentence)

@client.command(name="python", brief="The Snom will execute Python commands!")
async def remote_command(ctx, *,cmd=None):
    try:
        if cmd != None:
            await ctx.send(f"""```py
{eval(cmd)}
```""")
        if "CLOSE" in cmd.upper():
            raise ValueError("Are you foolish? Do you want the Snom to die?")
    except Exception:
        try:
            exc_info=sys.exc_info()
            try:
                raise SyntaxError("raised")
            except:
                pass
        finally:
            await ctx.send(f"""```py
{traceback.print_exception(*exc_info)}
```""")
            del exc_info

@client.command(name="stop", brief="This completely stop the bot.")
async def stop_bot(ctx):
    """
    This completely stop the bot.
    No argument required but being the developer is required :)
    """
    if ctx.message.author.id == 332082083604463616:
        await ctx.send("The Snom is going to sleep.")
        await client.close()






keep_alive()
client.run('NjU2OTM3NTU3MDk0ODI2MDE0.Xf5D4w.V-2bH2v5h5ab4B67bHkgBuLz_Yo')
