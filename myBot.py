import discord
import firebase_admin
import random
import datetime
from discord.ext import commands
from discord.ext.commands import check
from firebase_admin import credentials
from firebase_admin import firestore

TOKEN = 'Enter Token Here'

#Firestore setup
creds = credentials.Certificate("<Firestore credentials file>.json")
firebase_admin.initialize_app(creds)
db = firestore.client()

#Client/Bot
intents = discord.Intents().all()
client = commands.Bot('$', intents=intents)

client.remove_command('help')



def checkChannel(id):
	# Used for commands to check if command should
	# Operate in the following channels. In my server it is
	# bot-commands id and bot-testing id
    if id == '<#bot-commands channel ID goes here>' or id == '<#bot-testing channel ID goes here>':
        return True
    else:
        return False


#Event Example
@client.event
async def on_ready():
    print('King Khan is ready to go!')



#Command Example
@client.command('version')
async def version(context):
    await context.send('King Khan BOT is currently running on v1.0.0')

#====================================================================================================================

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content.lower().startswith('saaeed'):
        await message.channel.send('Saaeed. Thank you for your contribution.')

    if message.content.lower().startswith('rehan'):
        await message.channel.send('Rehan is my commander.')

    if message.content.lower().startswith('tareq'):
        await message.channel.send('Hey Tareq! How have you been?')

    if message.content.lower().startswith('pakistan'):
        await message.channel.send('Long Live Pakistan!')

    
    #Log Messages:
    channelName = message.channel.name

    content = message.content
    messageAuthor = str(message.author.name) + str(message.author.discriminator)

    newMessageDocument = db.collection('Messages').document()
    newMessageDocument.set({
        'Channel': channelName,
        'Content': content,
        'Time' : message.created_at,
        'User': messageAuthor
    })


    await client.process_commands(message)


@client.event
async def on_member_join(member):
    welcomeChannel = client.get_channel('< ENTER WELCOME CHANNEL ID HERE >')
    await welcomeChannel.send(f"Hey! Welcome to the server {member.mention}.")

@client.command(name='getName', pass_context=False, description='Get the name and ID of your user', aliases=['name', 'Name'])
@commands.has_role('Owner')
async def getName(context):
    if not checkChannel(context.message.channel.id):
        return


    await context.send(context.author.name)
    await context.send(context.author)


@client.command(name='warn', pass_context=True, description='warn a user')
@commands.has_permissions(kick_members=True)
@commands.has_any_role('Owner', 'Administrator', 'Moderator')
async def warn(context, member: discord.Member, *, reason='None specified'):
    if not checkChannel(context.message.channel.id):
        return

    if member.bot:
        await context.send("You can't warn a bot. Nice try.")
        return

    if member.top_role > context.author.top_role or member.id == 'ENTER ID OF THE SERVER OWNER':
        await context.send("You can't perform this on someone with higher level of authority than you")
        return

    if member.id == context.author.id:
        await context.send("Don't do that to yourself... Tell someone with higher authority instead!")
        return

    memberID = str(member.id)
    warningsDoc = db.collection('Users').document(memberID)
    doc = warningsDoc.get()
    if doc.exists:
        if 'Warnings' in doc.to_dict():
            warnings = doc.to_dict()['Warnings']
            warnings.append(reason)
            if len(warnings) == 5:
                warnings = []
                await member.ban(reason='Too many warnings!')
            warningsDoc.update({'Warnings': warnings})
        else:
            warningsDoc.update({'Warnings': [reason]})
    else:
        warningsDoc.set({'Warnings': [reason]})



@client.command(name='ban', pass_context=True, description='Ban a user', aliases=['Ban'])
@commands.has_permissions(ban_members=True)
@commands.has_any_role('Owner', 'Administrator', 'BOTS')
async def ban(context, member: discord.Member, *, reason=None):
    if not checkChannel(context.message.channel.id):
        return


    if member.top_role < context.author.top_role:
        await member.ban(reason=reason)
        await context.send('User ' + member.display_name + ' has been banned.')
    else:
        await context.send('You are not allowed to perform this.')

@client.command(name='kick', pass_context=True, description='Kick a user', aliases=['Kick', 'boot', 'Boot'])
@commands.has_permissions(kick_members=True)
@commands.has_any_role('Owner', 'Administrator', 'Moderator', 'BOTS')
async def kick(context, member: discord.Member):
    if not checkChannel(context.message.channel.id):
        return


    if member.top_role < context.author.top_role:
        await member.kick()
        await context.send('User ' + member.display_name + ' has been kicked.')
    else:
        await context.send('You are not allowed to use this.')


@client.command(name='gamertag', pass_context=False, description="Get all of Yasher's gamertags.", aliases=['Gamertag', 'gt', 'GT'])
async def gamertag(context):
    if not checkChannel(context.message.channel.id):
        return

    steamFriendCode = '304479258'
    battlenetID = 'YasherK#1970'
    activisionID = 'YasherK#1240451'
    valorantID = 'YasherK#4071'

    gamertagEmbed = discord.Embed(title="YasherK's Gamertags!", description="Add Yasher on each platform to play with him!", color=0x21bcdb)
    gamertagEmbed.add_field(name='Steam ID:', value='304479258', inline=True)
    gamertagEmbed.add_field(name='Battle Net ID:', value=battlenetID, inline=True)
    gamertagEmbed.add_field(name='Activision ID:', value=activisionID, inline=True)
    gamertagEmbed.add_field(name='Valorant ID:', value=valorantID, inline=True)
    gamertagEmbed.set_thumbnail(url='https://www.kindpng.com/picc/m/17-175295_transparent-videogame-clipart-icon-video-game-png-png.png')

    await context.send(embed=gamertagEmbed)

@client.command(name='socials', pass_context=False, description="Get all of Yasher's social media. Check him out!", aliases=['Socials', 'social', 'Social', 'Media', 'media'])
async def socials(context):
    if not checkChannel(context.message.channel.id):
        return


    socialEmbed = discord.Embed(title='My Social Media', description="Check out Yasher's social media platforms!", color=0xCA004D)
    socialEmbed.add_field(name="YouTube", value = "[Yasher's YouTube channel!](https://www.youtube.com/channel/UCVHcnpYVg5wvoTcLnTxQyQg)")
    socialEmbed.add_field(name="Twitch", value="[Yasher's Twitch channel!](https://www.twitch.tv/imyasher)")
    socialEmbed.add_field(name='Instagram', value = "[Yasher's Instagram!](https://www.instagram.com/yasher.khan/)")
    socialEmbed.set_thumbnail(url='https://www.channelpartnersonline.com/files/2017/08/Social-Media-Icons.jpg')
    
    await context.send(embed=socialEmbed)

@client.command(name='saaeed', pass_context=False, description= 'All about Saaeed.', aliases=['SAAEED', 'saed', 'saeed', 'saaed', 'Saed', 'Saeed', 'Saaed'])
async def saaeed(context):
    if not checkChannel(context.message.channel.id):
        return


    wordList = [
        'Hi Saaeed',
        'How are you Saaeed?',
        'Welcome sir!',
        'Call out boss',
        'I am a supervisor',
        'I am too good for you saaeed.'
        ]

    
    await context.send(random.choice(wordList))


@client.command(name='delete', pass_context=True, aliases=['del', 'remove', 'rm'], description='Removes Messages')
@commands.has_any_role('Moderator')
async def delete(context, amount=1):
    if amount <= 10 and amount >= 0:
        await context.channel.purge(limit=amount+1)
    else:
        await context.send('amount must be between 0 and 10.')



@client.command(name='clear', pass_context=False, aliases=['cls'])
@commands.has_any_role('Moderator')
async def clear(context):
    amount = 11
    await context.channel.purge(limit=amount)




@client.command(name='flip', pass_context=False, description='Flip a coin.', aliases=['coin', 'coinflip', 'flipcoin'])
async def flip(context):
    if not checkChannel(context.message.channel.id):
        return


    coin = ['Heads', 'Tails']
    await context.send(random.choice(coin))



#context.author.voice.channel gets the voice channel the author is in.
#context.author.voice.channel.id is channel id

@client.command(name='deafen_all', pass_context=False, description='deafen everyone in the vc.', aliases=['deafall', 'deafAll', 'deafenall', 'deafenAll', 'd_all', 'd_All'])
@commands.has_any_role('Moderator')
async def deafen_all(context):
    if not checkChannel(context.message.channel.id):
        return


    if context.author.voice == None:
        await context.send('You must be in a voice channel to use this command.')
        return

    voiceChannel = context.author.voice.channel
    for member in voiceChannel.members:
        await member.edit(deafen=True)

@client.command(name='undeafen_all', pass_context=False, description='undeafen everyone in the vc.', aliases=['undeafall', 'undeafAll', 'undeafenall', 'undeafenAll', 'ud_all', 'ud_All'])
@commands.has_any_role('Moderator')
async def undeafen_all(context):
    if not checkChannel(context.message.channel.id):
        return


    if context.author.voice == None:
        await context.send('You must be in a voice channel to use this command.')
        return

    voiceChannel = context.author.voice.channel
    for member in voiceChannel.members:
        await member.edit(deafen=False)

@client.command(name='mute_all', pass_context=False, description='mute everyone in the vc', aliases=['muteall', 'muteAll', 'm_all', 'm_All', 'mAll'])
@commands.has_any_role('Moderator')
async def mute_all(context):
    if not checkChannel(context.message.channel.id):
        return


    if context.author.voice == None:
        await context.send('You must be in a voice channel to use this command.')
        return
    
    voiceChannel = context.author.voice.channel
    for member in voiceChannel.members:
        await member.edit(mute=True)


@client.command(name='unmute_all', pass_context=False, description='unmute everyone in the vc', aliases=['unmuteall', 'unmuteAll', 'um_all', 'um_All, umAll'])
@commands.has_any_role('Moderator')
async def unmute_all(context):
    if not checkChannel(context.message.channel.id):
        return


    if context.author.voice == None:
        await context.send('You must be in a voice channel to use this command.')
        return

    voiceChannel = context.author.voice.channel
    for member in voiceChannel.members:
        await member.edit(mute=False)


@client.command(name='rdr', pass_context=False, description='Rubber Dingy Rapids Bro.', aliases=['rubber', 'RDR', 'Rubber', '4lions', '4Lions'])
async def rdr(context):
    if not checkChannel(context.message.channel.id):
        return
    
    await context.send('Rubber Dingy Rapids Bro.')

@client.command(name='help', pass_context=False)
async def help(context):
    if not checkChannel(context.message.channel.id):
        return
    
    helpText = '```json'
    helpText +='\n'
    for command in client.commands:
        helpText += f'"{command}" --> {command.description}\n'
    helpText += '```'

    await context.send(helpText)




#Run the bot on the server:
client.run(TOKEN)