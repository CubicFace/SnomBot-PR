import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
from math import *
from webserver import keep_alive
import os


client = commands.Bot(command_prefix=".s ", owner_id=332082083604463616)

client.remove_command('help')

welcome=discord.Object(656176795128692739)
bot_chnl=discord.Object(658069670469042206)
@client.event
async def on_ready():
    print("[INFO] On.")
    print(f"""
    [INFO] Bot info:
    User ID: {client.user.id}
    Name: {client.user.name}
    """)
    await client.send("The Snom is connected! <:NATSUKISPARKLE:656602806974808074>", channel=bot_chnl)

@client.event
async def on_member_join(member):
    print(f'[INFO] {member} joined. ({member.id})')
    await welcome.send(f"<@!{member.id}> <:NATSUKISPARKLE:656602806974808074> Welcome to __**SnomMania!**__ <:OwO:656758711444045835>")

@client.event
async def on_member_remove(member):
    print(f'[INFO] {member} left. ({member.id})')
    await welcome.send(f'{member} left the server... <:ZEROTWOCRY:656860514902867988>')

@client.command(name="help", brief="The Snom is here to help.")
async def help(ctx, cmd=None):
    embed=discord.Embed(colour=discord.Colour(0xbfcdff), title="Help", description="Here's the list of available commands.")
    for command in ctx.bot.commands:
        embed.add_field(name=f"{command}", value=f"{command.brief}", inline=True)
    embed.set_footer(text=f"The command prefix is {client.command_prefix}")
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
  sentences=['OwO',
  'UwU',
  ":3",
  "^_^",
  '*Hiii!*',
  "<@!401686680580521984> patate",
  "am bean baby .3.",
  "hewo gimme cuwy"]
  chosed_sentence=random.choice(sentences)
  print(f"[INFO][COMMAND]'hi' command by {ctx.message.author.name}. Chosen sentence: '{chosed_sentence}'")
  await ctx.send(chosed_sentence)

@client.command(name="python", brief="[DEV]The Snom will execute Python commands!")
async def remote_command(ctx, *,cmd=None):
    """
    The Snom will execute Python commands!
    Arguments:
    <cmd>: any Python command
    Being the developer is required! :)
    """
    if ctx.message.author.id == client.owner_id:
        try:
            if cmd != None:
                await ctx.send(f"""```py
{eval(cmd)}
```""")
            if cmd is None:
                await ctx.send("The Snom can't execute nothing, please give him something to execute.")
        except:
            await ctx.send("The command you were trying to execute got an error!\nAlso, you can't use functions such as defining variables, `import` and stuff like that.")
    else:
        await ctx.send("You are not the developer! Intruder! <:ANGWYSNOM:656753233968234516>")

@client.command(brief="Yummy waffles...")
async def waffle(ctx):
    """
    Yummy waffles...
    Call this command and the Snom will send Waffle pics.
    No arguments required.
    """
    image=discord.File(fp=f"wafflePics/waffle{random.randint(0,10)}.jpg")
    await ctx.send(":waffle:",file=image)

@client.command(name="stop", brief="[DEV]This completely stop the bot.")
async def stop_bot(ctx):
    """
    This completely stop the bot.
    No argument required but being the developer is required :)
    """
    if ctx.message.author.id == client.owner_id:
        await ctx.send("The Snom is going to sleep.")
        await client.close()
    else:
        await ctx.send("You are not the developer! Intruder! <:ANGWYSNOM:656753233968234516>")






keep_alive()
client.run('NjU2OTM3NTU3MDk0ODI2MDE0.Xf5D4w.V-2bH2v5h5ab4B67bHkgBuLz_Yo')
