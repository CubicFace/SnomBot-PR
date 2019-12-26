###########################################################################
########     This bot has been made specially  for a particular    ########
########                      server.                              ########
###########################################################################

########## Manassé Ratovo, also known as Gradient ##########
##       For personal and educational purposes only       ##
############################################################

## Basic Discord API modules
import discord
from discord.ext import commands
from discord.ext.commands import Bot
##

## Other modules
import random # Random module
from math import * # Math module to use advanced mathematical operations
from webserver import keep_alive # Web server for keeping the bot alive when inactive
import os # OS Module to get more flexibility in the Linux host (Heroku)
import json # JSON Module to read and write json files
##





########### Bot setup

##### Opening JSON files and storing them as dictionnairies variables
with open('package.json', 'r') as f: # Contains bot version and application (npm) name
    bot_json=json.load(f)
with open('properties.json', 'r') as f: # Contains ids
    botProp=json.load(f)
#####

##### Setting Bot instance
client = commands.Bot(command_prefix=".s ", owner_id=botProp['owner'])
#####

##### Predefining some useful variables
client.remove_command('help') # Remove help command to redefine it
guild_id=botProp['guildid'] # Server id
welcome_id=botProp['welcome'] # Welcome channel id
bot_chnl_id=botProp['botchannel'] # Bot command channel id
log_chnl=botProp['logid'] # Bot logs channel id
news_chnl=botProp['newschannel'] # News channel id
role_request=botProp['rolerequest'] # Role requests channel id
chnl_request=botProp['channelrequest'] # Channel requests channel id
emote_idea=botProp['emoteidea'] # Emote suggestions channel id
bot_request=botProp['botrequest'] # Bot requests channel id
#####

##### Actions mades when connected to Discord
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game("on_ready()")) # Changing status to Do Not Disturb
    
    print(f"[INFO] On.\nVersion: {bot_json['version']}") # Logs that the bot is on
    
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game("[INFO]ON")) # Changing activity
    
    print(f"""[INFO] Bot info:
Application name: {bot_json['name']}
User ID: {client.user.id}
Name: {client.user.name}""") # Logs some bot info.
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Connected.")) # Changing status to idle
    
    channel=client.get_channel(log_chnl) # Selects bot logs channel
    await channel.send(f"The Snom is connected! <:NATSUKISPARKLE:656602806974808074>\n`SnomBot {bot_json['version']}`") # Send connection message to that channel
    
    await client.change_presence(status=discord.Status.online, activity=discord.Game("with snow UwU.")) # Changing status to connected and displaying 'Playing with snow UwU'
###########



########### Basic events
###########

##### When member joins
@client.event
async def on_member_join(member):
    print(f'[INFO] {member} joined. ({member.id})') # Logs who joined with User ID
    
    channel=client.get_channel(welcome_id) # Selecting Welcome channel
    
    role=discord.utils.get(member.guild.roles, name="❄️🍼Baby Snom🍼❄️ (lvl. 1)") # Selecting role to add
    
    await channel.send(f"<@!{member.id}> <:NATSUKISPARKLE:656602806974808074> Welcome to __**SnomMania!**__ <:OwO:656758711444045835>") # Sending message to Welcome channel
    
    await member.add_roles(role, reason="New user") # Add role to joined user
#####

###### When member leaves 
@client.event
async def on_member_remove(member):
    print(f'[INFO] {member} left. ({member.id})') # Logs who left with User ID
    
    channel=client.get_channel(welcome_id) # Selecting Welcome channel
    
    await channel.send(f'{member} left the server... <:ZEROTWOCRY:656860514902867988>') # Sending message to Welcome Channel
######

###########
###########



########### Defining (asynchronous) commands
###########

##### Help command
@client.command(name="help", brief="The Snom is here to help.", usage="<cmd>: If passed, it'll return some details ona specific command, else it'll send the list of available commands for this bot.")
async def help(ctx, cmd=None):
    """
    The Snom is here to help.
    Ask for the list of availabble command or get help on a specific command.
    """
    if cmd is None: # If not passed
        print(f"[INFO][COMMAND]Help by {ctx.author.name}. Command argument not passed. Sending list of available commands.") # Logs
        
        embed=discord.Embed(colour=discord.Colour(0xbfcdff), title="Help", description="Here's the list of available commands.") # Embed creation
        
        ## Listing all bot commands
        for command in ctx.bot.commands:
            embed.add_field(name=f"{command}", value=f"{command.brief}", inline=True) # For each command it adds a field with the name and the brief description of it
        
        embed.set_footer(text=f"The command prefix is {client.command_prefix}\nSnomBot {bot_json['version']}") # Signature footer
        ##

        await ctx.send("The list of commands has been sent to your direct messages.")
        await ctx.message.author.send("Here are your commands, have fun.\n*Note: some commands must be sent in the server to work.*", embed=embed) # Send message

    else: # If passed
        
        foundCommand=False # Boolean created to ensure that the command exist
        
        for command in ctx.bot.commands: # Seaching in available commands
            if str(command).upper() == cmd.upper(): # If it matchs
                
                foundCommand=True # The boolean is true
                
                print(f"[INFO][COMMAND]Help by {ctx.author.name}. Command argument passed. Sending ") # Logs
                
                embed=discord.Embed(colour=discord.Colour(0xbfcdff), title=f"Command help: {cmd}", description=f"{command.help}") # Embed creation
                
                embed.add_field(name="Usage", value=command.usage, inline=True) # Adds an usage field with command usage
                
                embed.set_footer(text=f"The command prefix is {client.command_prefix}\nSnomBot {bot_json['version']}") # Prefix indication and signature footer
        
        if not foundCommand: # If the command is not found
            
            print(f"[INFO][COMMAND]Help by {ctx.author.name}. Command argument passed. '{cmd}' command not found.") # Logs
            
            await ctx.send(f"The Snom can't find the command `{cmd}`. Type `.s help` to see the available commands.") # Sends message to prevent user.
        
        else:            
            await ctx.send(embed=embed)
#####

##### Ping command
@client.command(brief="Ask the ping, and the Snom will pong!", usage="`.s ping`\nNo arguments required.")
async def ping(ctx):
    """
    Ask the ping, and the Snom will pong!
    It also returns de latency in ms.
    """
    
    print(f"[INFO][COMMAND]Ping by {ctx.message.author.name}. Actual bot latency: {client.latency * 1000} ms.") # Logs user with bot latency
    
    await ctx.send(f'The snom has Pong! ({round(client.latency * 1000,2)} ms)') # Sends rounded latency to the user
#####

##### Hi command
@client.command(brief="Say 'Hi' to the Snom.", usage="`.s hi`\nNo arguments required.")
async def hi(ctx):
    """
    Say 'Hi' to the Snom.
    This command send random sentence from the database.
    """
    sentences=[] # Creating list for storing sentences

    ## Sentences storing
    with open('hi_sentences.txt', 'r') as f: # Open the hi_sentences.txt file
        for line in f: # For each line in the file
            sentences.append(line.rstrip()) # Add it to the list
    ##


    chosed_sentence=random.choice(sentences) # Choosing a random sentence from the list
    
    print(f"[INFO][COMMAND]'hi' command by {ctx.message.author.name}. Chosen sentence: '{chosed_sentence}'") # Log
    
    await ctx.send(chosed_sentence) # Sending chosen sentence
#####

##### Python command
@client.command(name="python", brief="[DEV]The Snom will execute Python commands!", usage="`.s python <cmd>`\nArguments:\n<cmd>: any Python command\nBeing the developer is required! :)")
async def remote_command(ctx, *,cmd=None):
    """
    The Snom will execute Python commands!
    Note: this command can't define variables, import modules and stuff like that.
    """
    
    if ctx.message.author.id == client.owner_id: # If the user's ID matches with my account ID, in other terms, if it's me
        try:
            if cmd != None:
                await ctx.send(f"""```py
{eval(cmd)}
```""") # Sending python output of entered command
            if cmd is None: # If not passed (error handling)
                
                print("[INFO][COMMAND]Python: no command given") # Logs
                
                await ctx.send("The Snom can't execute nothing, please give him something to execute.") # Send message to user
        
        except Exception as e: # Error handling

            print(f"[INFO][COMMAND]Python: error: {e}") # Logs
            
            await ctx.send(f"The command you were trying to execute got an error!\nAlso, you can't use functions such as defining variables, `import` and stuff like that.\n```py\n{e}\n```") # Send message to user
    
    else: # If not me
        
        print(f"[INFO][COMMAND]Python: {ctx.author.name} tried to use command but is not the developper.") # Logs
        
        await ctx.send("You are not the developer! Intruder! <:ANGWYSNOM:656753233968234516>") # Send message to user
#####

##### Waffle command
@client.command(brief="Yummy waffles...", usage="`.s waffle`\nNo arguments required.")
async def waffle(ctx):
    """
    Yummy waffles...
    Call this command and the Snom will send Waffle pics.
    """
    
    image=discord.File(fp=f"wafflePics/waffle{random.randint(0,10)}.jpg") # Open random indexed image file

    print(f"[INFO][COMMAND]Waffle by {ctx.message.author.name}.") # Logs

    await ctx.send(":waffle:",file=image) # Sends image
#####

##### Guild command
@client.command(brief="The Snom knows a little bit about the server <:OwO:656758711444045835>", usage="`.s guild <attribute=None>`\nArguments:\n<attribute=None> To pass this argument, you need to provide a Discord API Guild attribute name to get the related info, else it'll retrun a bunch of default infos.")
async def guild(ctx, attribute=None):
    """
    The Snom knows a little bit about the server <:OwO:656758711444045835>
    This command gives you info about the server and some properties.
    """

    guild=client.get_guild(guild_id) # Creating server object/insatance
    
    embed=discord.Embed(coulour=discord.Colour(0x96fffc), title="Guild/server status", description="Here's what the Snom knows about the guild <:NATSUKISPARKLE:656602806974808074>") # Embed creation
    
    if attribute is None: # If not passed
        embed.set_thumbnail(url=str(guild.icon_url)) # Using server icon as thumbnail
        # Basic server info
        embed.add_field(name="Name", value=guild.name, inline=True)
        embed.add_field(name="Description", value=guild.description if guild.description != None else "No description.", inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Member count", value=str(len(guild.members)), inline=True)
        embed.add_field(name="Emoji count", value=str(len(guild.emojis)), inline=True)
        embed.add_field(name="Region", value=f'{guild.region}', inline=True)
        #
    
    else: # If passed
        exec(f"embed.add_field(name=\"{attribute}\", value=str(guild.{attribute}), inline=True)") # Creating field of specific attribute
    
    embed.set_footer(text=f"SnomBot {bot_json['version']}") # Signature footer
    
    print(f"[INFO][COMMAND]Guild by {ctx.message.author.name}. ".join("No attribute passed, sending defaults." if attribute is None else f"Searching guild attribute: {attribute}")) # Logs
    
    await ctx.send(embed=embed) # Send final message
#####

##### lewd based command
@client.command(aliases=["dickpic", "nude", "porn", "hentai"], brief="Do not do it! <:ANGWYSNOM:656753233968234516>", usage=">:[")
async def naughty(ctx):
    """
    Do not do it! <:ANGWYSNOM:656753233968234516>
    The Snom won't like it.
    """

    print(f"[INFO][COMMAND]{ctx.message.author.name} tried to tempt the Snom: >:[") # Logs

    await ctx.send("<:ANGWYSNOM:656753233968234516> The Snom is __**Christian**__ :cross: ") # Send message
#####

##### Say command
@client.command(brief="Make the Snom say something.", usage="`.s say <*,say>`\nArguments:\n<*, say>: The thing you want to say")
async def say(ctx, *,say):
    """
    Make the Snom say something
    Also it's indirect an use of Administrator role.
    """

    print(f"[INFO][COMMAND]{ctx.author.name} said: '{say}''") # Logs
    
    await ctx.send(say) # Sends what the user entered.
#####

##### Suggest command
@client.command(brief="Suggest anything, and the Snom will say it louder in a more important channel.", usage="`.s suggest <type=server> <*,suggestion>`\nArguments:\n<sgtype=server>: Choose wich type of suggestion you want to send. Types are: server, bot, bot_feature, role, channel, emote.\n<*,suggestion>: The content of your suggestion.\nNote: For emote suggestion you need to attach a file and write your suggestion text anyways, otherwise it won't work.")
async def suggest(ctx, sgtype: str="server",*,suggestion):
    """
    Suggest anything, and the Snom will say it louder in a more important channel.
    You can suggest roles, bot features, emotes etc.
    """
    
    known_type=False # Setting bool to know if a type is known

    #/# Basically, it create different Embed instances depending on the type wanted, selects the appropriate channel, and set the boolean on true
    if sgtype.upper() == "ROLE":
        known_type=True
        embed=discord.Embed(colour=discord.Colour(0xff7147), title="Role suggestion", description=suggestion)
        channel=client.get_channel(role_request)
    
    elif sgtype.upper() == "BOT_FEATURE":
        known_type=True
        embed=discord.Embed(colour=discord.Colour(0xff7147), title="Bot (feature) suggestion", description=suggestion)
        channel=client.get_channel(bot_request)
    
    elif sgtype.upper() == "BOT":
        known_type=True
        embed=discord.Embed(colour=discord.Colour(0xff7147), title="Bot suggestion", description=suggestion)
        channel=client.get_channel(bot_request)
    
    elif sgtype.upper() == "EMOTE":
        known_type=True
        embed=discord.Embed(colour=discord.Colour(0xff7147), title="Emote suggestion", description=suggestion)
        for a in ctx.message.attachments: # Searching in all attachments (if multiple have been attached)
            embed.set_image(url=str(a.url)) # Adds an image if attached
        channel=client.get_channel(emote_idea)
    
    elif sgtype.upper() == "CHANNEL":
        known_type=True
        embed=discord.Embed(colour=discord.Colour(0xff7147), title="Channel suggestion", description=suggestion)
        channel=client.get_channel(chnl_request)
    
    elif sgtype.upper() == "SERVER":
        known_type=True
        embed=discord.Embed(colour=discord.Colour(0xff7147), title="Server suggestion", description=suggestion)
        channel=ctx
    #/#

    if known_type: # If the type is known
        
        embed.set_thumbnail(url=str(ctx.message.author.avatar_url)) # Setting user avatar as thumbnail
        
        embed.set_footer(text=f"SnomBot {bot_json['version']}") # Signature footer
        
        print(f"[INFO][COMMAND]Suggestion by {ctx.author.name}. Suggested a '{sgtype}': \"{suggestion}\"") # Logs
        
        sent_msg=await channel.send(f"@here {ctx.author.mention} suggested:", embed=embed) # Sending message and sotring it into a variable
        
        if channel != ctx:
            await ctx.send(f"Your suggestion has been sent. Check <#{channel.id}>")
        
        ## Unicode emojis
        check_emoji='\N{WHITE HEAVY CHECK MARK}' 
        x_emoji='\N{CROSS MARK}'
        ##
        
        ## Adding reactions for voting
        await sent_msg.add_reaction(check_emoji)
        
        await sent_msg.add_reaction(x_emoji)
        ##

        await channel.send("⬆️Vote with the reacions above.⬆️")
    
    else: # If the type is unknown
        
        print(f"[INFO][COMMAND]Suggestion by {ctx.author.name}. Wrong '{sgtype}' type.") # Logs
        
        await ctx.send(f"The Snom can't suggest a {sgtype}") # Sends message
#####

##### Shout command, admin based
@client.command(aliases=["shout"], brief="[ADMIN]Let the Snom shout something in the news!", usage="Being an Administrator is required.\n`.s notice <level> <target> <*,msg>`\nArguments:\n<level>: Level of mention\n0: prints `[INFO]`\n1: make an `@here` ping\n2: make an `@everyone` ping\n<target>: Where you want the bot to shout\nserver: sent in <#656377626667253769>\nbot: sent in <#658405098258432000>\n<*,msg>: the content of your shout.")
@commands.has_permissions(administrator=True) # Needs admin permissions
async def notice(ctx, level, target, *,msg):
    """
    Let the Snom shout something in the news!
    Need to let everyone know something in a cool way? <:SNIPPITYSNAPSUICIDEINTHESNACC:656962832914710548>
    The Snom will shout it either in <#656377626667253769> or in <#658405098258432000> 
    """
    global _temp_author # Setting a temporary author variable
    _temp_author=ctx.author.name # Assigning it to the command author
    
    ## Mention level
    if int(level) == 0:
        str_msg="[INFO]"
    elif int(level) == 1:
        str_msg="@here "
    elif int(level) == 2:
        str_msg="@everyone "
    ##

    ## Type and target
    if str(target).upper() == 'SERVER':
        
        channel=client.get_channel(news_chnl) # Selecting News Channel
        
        embed=discord.Embed(colour=discord.Colour(0xff0000), title="Server update", description=msg) # Embed creation
    
    elif str(target).upper() == 'BOT':
        
        channel=client.get_channel(log_chnl) # Selecting Bot logs channel
        
        embed=discord.Embed(colour=discord.Colour(0xa200ff), title="Bot update", description=msg) # Embed creation
    
    embed.set_thumbnail(url=str(ctx.message.author.avatar_url)) # Using user avatar as thumbnail
    
    embed.set_footer(text=f"SnomBot {bot_json['version']}") # Signature footer
    
    print(f"[INFO][COMMAND(Admin)]{target} shout of level {level} by {ctx.message.author.id}: '{msg}'") # Logs
    
    await channel.send(f"{str_msg} {ctx.author.mention} shouted:", embed=embed) # Sends message in selected channel
## If not administrator
@notice.error
async def notice_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        
        print(f"[INFO][COMMAND(Admin)]{_temp_author} tried to shout but do not have permissions.") # Logs
        
        await ctx.send("You are not an administrator! <:ANGWYSNOM:656753233968234516>") # Sends message
        
        del _temp_author # Deletes variable
##
#####

##### Menacing command
@client.command(brief="Yare yare daze", usage="`.s menacing <emoji>`\nArguments:\n<emoji>: The emoji you want to be surrounded")
async def menacing(ctx, emoji):

    print(f"[INFO][COMMANDS]Menacing by {ctx.author.name}. Emoji: '{emoji}'") # Logs

    await ctx.send("<:MANASSING:656760045475987476> <:MANASSING:656760045475987476> <:MANASSING:656760045475987476>")
    await ctx.send(f"<:MANASSING:656760045475987476> {emoji} <:MANASSING:656760045475987476>")
    await ctx.send("<:MANASSING:656760045475987476> <:MANASSING:656760045475987476> <:MANASSING:656760045475987476>")
#####

##### Stop command
@client.command(name="stop", brief="[DEV]This completely stop the bot.", usage="No argument required but being the developer is required :)")
async def stop_bot(ctx):
    f"""
    This completely stop the bot.
    By closing the connection, <@!{client.owner_id}> will need to restart the host to make the bot start again.
    """
    if ctx.message.author.id == client.owner_id: # If it's me
        
        await ctx.send("The Snom is going to sleep.") # Sends message
        
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game("Stopping")) # Changing status to Do Not Disturb
        
        await client.change_presence(status=discord.Status.offline) # Changing status to offline
        
        await client.close() # Closing connection between the host and Discord
    else: # If it's not me
        await ctx.send("You are not the developer! Intruder! <:ANGWYSNOM:656753233968234516>\nYou are trying to kill the Snom!!!") # Sends message
#####

###########
###########




########### Run bot indefinitely
keep_alive() # Start the Web Server
client.run(botProp['token']) # Opens connection to Discord
###########
