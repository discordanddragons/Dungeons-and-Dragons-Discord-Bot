# Work with Python 3.6
import discord
import asyncio
TOKEN = 'NTYzMDUxMTA2ODkzMDM3NTk4.XKTzBA.kCuGuv8Onok8NZZm1Q5TfPfrGAc'

# TODO Still need to do some role stuff to make sure people can't join things that they shouldn't be able to

client = discord.Client()


# Character creation stuff
characterDict = {}


class Character:
    def __init__(self, name, owner, active=0):
        self.name = name
        self.owner = owner
        self.active = active

    class Stats:
        def __init__(self, stre=10, dex=10, con=10, inte=10, wis=10, cha=10):
            self.strength = stre
            self.dexterity = dex
            self.constitution = con
            self.intelligence = inte
            self.wisdom = wis
            self.charisma = cha

    #class Skills:

    #class Items:


@client.event
async def on_voice_state_update(before, after):
    isDM = False
    isPlayer = False
    for role in before.roles:
        print(role.name)
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
            await client.move_member(member, destChannel)
            print("moving ", member, " to: ", destChannel)


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
    # administrator/DM commands
    if message.author.server_permissions.administrator or isDM:
        if message.content.startswith("!registerLanguage"):
            channelname = "language_" + message.content.replace("!registerLanguage", "").lower()
            newChannel = await client.create_channel(message.server, channelname, type=discord.ChannelType.voice)
            role = await client.create_role(message.server, name=channelname)
            newRole = await client.add_roles(message.author, role)
            roles = message.server.roles
            newChannel.overwrites_for(newRole)
            overwrite = discord.PermissionOverwrite()
            overwrite.connect = False
            # if there is a reason to make chats hidden until joined then uncomment this
            # overwrite.read_messages = False

            for role in roles:
                if role.is_everyone:
                    await client.edit_channel_permissions(newChannel, role, overwrite)
                    break

        if message.content.startswith("!removeLanguage"):
            language = "language_" + message.content.replace("!registerLanguage", "").lower()
            for server in client.servers:
                client.delete_role(server, language)
                client.delete_channel(language)
            await client.send_message(message.channel, "Removed " + language)

    if isPlayer:
        # player specific commands
        # print("check that the language role already exists, and add the appropriate role to the user")
        if message.content.startswith("!iknow"):
            language = "language_" + message.content.replace("!iknow", "").lower()
            roleSet = 0
            for server in client.servers:
                for role in server.roles:
                    if language in role.name:
                        await client.send_message(message.channel, message.author.name + " now knows " + language[9:])
                        await client.add_roles(message.author, role)
                        roleSet = 1
                        break
                if roleSet == 0:
                    await client.send_message(message.channel, "Do you speak english in what?")


        # 
        if message.content.startswith("!newCharacter"):
            characterName = message.content.replace("!newCharacter", "")
            character = Character(characterName, message.author)
            characterDict[characterName] = character
            await client.send_message(message.channel, characterName + " has risen.")

        if message.content.startswith("!active"):
            characterName = message.content.replace("!active", "")
            if characterName in characterDict:
                if characterDict[characterName].owner == message.author:
                    for character in characterDict:
                        # set all other characters to inactive
                        if characterDict[character].owner == message.author and characterDict[character].active == 1:
                            characterDict[character].active = 0
                    # set the specified character to active
                    characterDict[characterName].active = 1
                    await client.send_message(message.channel, characterName + " is now active.")
                else:
                    await client.send_message(message.channel, characterName + " is not one of your characters.")
            else:
                await client.send_message(message.channel, characterName + " does not exist.")

# TODO be able to return a list of all of the characters owned by a specific user
        if message.content.startswith("!characters"):
            # shows all the characters that are owned by a user
            user = message.content.replace("!characters", "")
            for character in characterDict:
                if characterDict[character].owner == user:
                    await client.send_message(message.channel, user + " owns " + characterDict[character].name)

    # everyone commands
    if message.content.startswith("!help"):
        DMCommands = "DM Commands\n"
        DMCommands += "!registerLanguage language_name \n\t- Adds a language channel, users must know this language in order to join this voice channel\n"
        DMCommands += "!deleteLanguage language_name \n\t- Removes language channel and roles associated to that language\n"
        PlayerCommands = "Player Commands\n"
        PlayerCommands += "!iknow language_name \n\t- Adds your player to the language role\n"
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
        # first ensure that the roles exist for DM and players
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
        # now that the roles exist give the DM role to the creator of the sever, and player to all other members
        for member in client.get_all_members():
            if member.server_permissions.administrator:
                await client.add_roles(member, DMRole)
            else:
                await client.add_roles(member, PlayerRole)
client.run(TOKEN)
