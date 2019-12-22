import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
from math import *
from webserver import keep_alive
import os
import json

with open('package.json', 'r') as f:
    bot_json=json.load(f)
with open('properties.json', 'r') as f:
    botProp=json.load(f)

client = commands.Bot(command_prefix=".s ", owner_id=botProp['owner'])

client.remove_command('help')
guild_id=botProp['guildid']
welcome_id=botProp['welcome']
bot_chnl_id=botProp['botchannel']


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game("on_ready()"))
    print(f"[INFO] On.\nVersion: {bot_json['version']}")
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game("[INFO]ON"))
    print(f"""[INFO] Bot info:
Application name: {bot_json['name']}
Version: {bot_json['version']}
User ID: {client.user.id}
Name: {client.user.name}""")
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Connected."))
    channel=client.get_channel(bot_chnl_id)
    await channel.send(f"The Snom is connected! <:NATSUKISPARKLE:656602806974808074>\n*SnomBot {bot_json['version']}*")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("with snow UwU."))

@client.event
async def on_member_join(member):
    print(f'[INFO] {member} joined. ({member.id})')
    channel=client.get_channel(welcome_id)
    await channel.send(f"<@!{member.id}> <:NATSUKISPARKLE:656602806974808074> Welcome to __**SnomMania!**__ <:OwO:656758711444045835>")

@client.event
async def on_member_remove(member):
    print(f'[INFO] {member} left. ({member.id})')
    channel=client.get_channel(welcome_id)
    await channel.send(f'{member} left the server... <:ZEROTWOCRY:656860514902867988>')


@client.command(name="help", brief="The Snom is here to help.", usage="<cmd>: If passed, it'll return some details ona specific command, else it'll send the list of available commands for this bot.")
async def help(ctx, cmd=None):
    """
    The Snom is here to help.
    Ask for the list of availabble command or get help on a specific command.
    """
    if cmd is None:
        print(f"[INFO][COMMAND]Help by {ctx.author.name}. Command argument not passed. Sending list of available commands.")
        embed=discord.Embed(colour=discord.Colour(0xbfcdff), title="Help", description="Here's the list of available commands.")
        for command in ctx.bot.commands:
            embed.add_field(name=f"{command}", value=f"{command.brief}", inline=True)
        embed.set_footer(text=f"The command prefix is {client.command_prefix}\nSnomBot {bot_json['version']}")

    else:
        foundCommand=False
        for command in ctx.bot.commands:
            if str(command).upper() == cmd.upper():
                foundCommand=True
                print(f"[INFO][COMMAND]Help by {ctx.author.name}. Command argument passed. Sending ")
                embed=discord.Embed(colour=discord.Colour(0xbfcdff), title=f"Command help: {cmd}", description=f"{command.help}")
                embed.add_field(name="Usage", value=command.usage, inline=True)
                embed.set_footer(text=f"The command prefix is {client.command_prefix}\nSnomBot {bot_json['version']}")
        if not foundCommand:
            print(f"[INFO][COMMAND]Help by {ctx.author.name}. Command argument passed. '{cmd}' command not found.")
            await ctx.send(f"The Snom can't find the command `{cmd}`. Type `.s help` to see the available commands.")
    await ctx.send(embed=embed)

@client.command(brief="Ask the ping, and the Snom will pong!", usage="No arguments required.")
async def ping(ctx):
    """
    Ask the ping, and the Snom will pong!
    It also returns de latency in ms.
    """
    print(f"[INFO][COMMAND]Ping by {ctx.message.author.name}. Actual bot latency: {client.latency * 1000} ms.")
    await ctx.send(f'The snom has Pong! ({round(client.latency * 1000,2)} ms)')

@client.command(brief="Say 'Hi' to the Snom.", usage="No arguments required.")
async def hi(ctx):
  """
  Say 'Hi' to the Snom.
  This command send random sentence from the database.
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

@client.command(name="python", brief="[DEV]The Snom will execute Python commands!", usage="Arguments:\n<cmd>: any Python command\nBeing the developer is required! :)")
async def remote_command(ctx, *,cmd=None):
    """
    The Snom will execute Python commands!
    Note: this command can't define variables, import modules and stuff like that.
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

@client.command(brief="Yummy waffles...", usage="No arguments required.")
async def waffle(ctx):
    """
    Yummy waffles...
    Call this command and the Snom will send Waffle pics.
    """
    image=discord.File(fp=f"wafflePics/waffle{random.randint(0,10)}.jpg")
    print(f"[INFO][COMMAND]Waffle by {ctx.message.author.name}.")
    await ctx.send(":waffle:",file=image)

@client.command(brief="The Snom knows a little bit about the server <:OwO:656758711444045835>", usage="Arguments:\n<attribute=None> To pass this argument, you need to provide a Discord API Guild attribute name to get the related info, else it'll retrun a bunch of default infos.")
async def guild(ctx, attribute=None):
    """
    The Snom knows a little bit about the server <:OwO:656758711444045835>
    This command gives you info about the server and some properties.
    """
    guild=client.get_guild(guild_id)
    embed=discord.Embed(coulour=discord.Colour(0x96fffc), title="Guild/server status", description="Here's what the Snom knows about the guild <:NATSUKISPARKLE:656602806974808074>")
    if attribute is None:
        embed.set_thumbnail(url=str(guild.icon_url))
        embed.add_field(name="Name", value=guild.name, inline=True)
        embed.add_field(name="Description", value=guild.description if guild.description != None else "No description.", inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Member count", value=str(len(guild.members)), inline=True)
        embed.add_field(name="Emoji count", value=str(len(guild.emojis)), inline=True)
        embed.add_field(name="Region", value=f'{guild.region}', inline=True)
    else:
        exec(f"embed.add_field(name=\"{attribute}\", value=str(guild.{attribute}), inline=True)")
    embed.set_footer(text=f"SnomBot {bot_json['version']}")
    print(f"[INFO][COMMAND]Guild by {ctx.message.author.name}. ".join("No attribute passed, sending defaults." if attribute is None else f"Searching guild attribute: {attribute}"))
    await ctx.send(embed=embed)

@client.command(name="dickpic", brief="Do not do it! <:ANGWYSNOM:656753233968234516>", usage=">:[")
async def naughty(ctx):
    """
    Do not do it! <:ANGWYSNOM:656753233968234516>
    The Snom won't like it.
    """
    print(f"[INFO][COMMAND]{ctx.message.author.name} tried to tempt the Snom: >:[")
    await ctx.send("<:ANGWYSNOM:656753233968234516> The Snom is __**Christian**__ :cross: ")

@client.command(brief="Make the Snom say something.", usage="Arguments:\n<id=None>: If passed, it'll send the message to a channel in the current guild.\n<*, say>: The thing you want to say")
async def say(ctx, id=None, *,say):
    """
    Make the Snom say something
    Also it's indirect an use of Administrator role.
    """
    if id != None:
        channel=client.get_channel(id)
        await channel.send(say)
    await ctx.send(say)

@client.command(name="stop", brief="[DEV]This completely stop the bot.", usage="No argument required but being the developer is required :)")
async def stop_bot(ctx):
    f"""
    This completely stop the bot.
    By closing the connection, <@!{client.owner_id}> will need to restart the host to make the bot start again.
    """
    if ctx.message.author.id == client.owner_id:
        await ctx.send("The Snom is going to sleep.")
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game("Stopping"))
        await client.change_presence(status=discord.Status.offline)
        await client.close()
    else:
        await ctx.send("You are not the developer! Intruder! <:ANGWYSNOM:656753233968234516>")






keep_alive()
client.run(botProp['token'])
