# Work with Python 3.6
import discord
import asyncio
TOKEN = 'NTYzMDUxMTA2ODkzMDM3NTk4.XKTzBA.kCuGuv8Onok8NZZm1Q5TfPfrGAc'

client = discord.Client()

@client.event         
async def on_voice_state_update(before, after):
    isDM = False
    isPlayer = False
    for role in before.roles:
        print (role.name)
        if role.name == "Bots":
            return
        elif role.name == "DM":
            isDM = True
        elif role.name == "Player":
            isPlayer = True
    if before.server_permissions.administrator or isDM:
        destChannel = after.voice.voice_channel
        if destChannel == None:
            return
        for member in client.get_all_members():
            if member == before or member.voice.voice_channel == None:
                continue
            await client.move_member(member,destChannel)
            print ("moving ",member," to: ",destChannel)
        
@client.event         
async def on_message(message):
    if message.author == client.user:
        return
    isDM = False
    isPlayer = False
    for role in message.author.roles:
        if role.name == "DM":
            isDM = True
        if role.name == "Player":
            isPlayer = True
    #administrator/DM commands
    if message.author.server_permissions.administrator or isDM:        
        if message.content.startswith("!registerLanguage"):
            channelname = message.content.replace("!registerLanguage","")
            newChannel = await client.create_channel(message.server, channelname, type=discord.ChannelType.voice)
            role = await client.create_role(message.server, name=channelname)
            newRole = await client.add_roles(message.author, role)
            roles = message.server.roles
            newChannel.overwrites_for(newRole)
            overwrite = discord.PermissionOverwrite()
            overwrite.connect = False
            #if there is a reason to make chats hidden until joined then uncomment this
            #overwrite.read_messages = False
            
            for role in roles:
                if role.is_everyone:
                    await client.edit_channel_permissions(newChannel, role, overwrite)
                    break
    else:
        #player specific commands
        if message.content.startswith("!registerLanguage"):
            print("check that the language role already exists, and add the appropriate role to the user")
        
    #everyone commands
    if message.content.startswith("!help"):
        DMCommands = "DM Commands\n"
        DMCommands += "!registerLanguage language_name \n\t- Adds a language channel, users must know this laguage in order to join this voice channel\n"
        PlayerCommands = "Player Commands\n"
        PlayerCommands += "!registerLanguage language_name \n\t- Adds your player to the language role\n"
        DMCommands + PlayerCommands
        await client.send_message(message.channel, DMCommands +PlayerCommands)

@client.event         
async def on_member_join(member):
    for role in member.server.roles:
        if role.name == "Player":
            await client.add_roles(member, role)

@client.event
async def on_ready():
    for server in client.servers:
        #first ensure that the roles exist for DM and players
        hasDM = False
        hasPlayer = False
        DMRole = None
        PlayerRole = None
        for role in server.roles:
            if role.name == "DM":
                DMRole = role
                hasDM = True
            elif role.name == "Player":
                PlayerRole = role
                hasPlayer = True
        if hasDM == False:
            DMRole = await client.create_role(server, name="DM")
        if hasPlayer == False:
            PlayerRole = await client.create_role(server, name="Player")
        #now that the roles exist give the DM role to the creator of the sever, and player to all other members
        for member in client.get_all_members():
            if member.server_permissions.administrator:
                await client.add_roles(member, DMRole)
            else:
                await client.add_roles(member, PlayerRole)
client.run(TOKEN)
