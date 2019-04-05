# Work with Python 3.6
import discord
from characterManager import characterManager
TOKEN = 'NTYzMDUxMTA2ODkzMDM3NTk4.XKTzBA.kCuGuv8Onok8NZZm1Q5TfPfrGAc'

# TODO Still need to do some role stuff to make sure people can't join things that they shouldn't be able to

client = discord.Client()


# Character creation stuff
characters = characterManager()

@client.event
async def on_voice_state_update(before, after):
    isDM = False
    isPlayer = False
    for role in before.roles:
        if role.name == "DM":
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
        if message.content.startswith("!registerLanguage "):
            channelname = "language_" + message.content.replace("!registerLanguage ", "").lower()
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

        if message.content.startswith("!removeLanguage "):
            language = "language_" + message.content.replace("!registerLanguage ", "").lower()
            for server in client.servers:
                client.delete_role(server, language)
                client.delete_channel(language)
            await client.send_message(message.channel, "Removed " + language)

    if isPlayer:
        # player specific commands
        if message.content.startswith("!"):
            temp = characters.getCharacters(message.author)
            for character in temp:
                if message.author == characters.getOwner(character) and characters.getActive(character) is True:
                    if message.content.startswith("!iknow "):
                        language = "language_" + message.content.replace("!iknow ", "").lower()
                        roleSet = 0
                        for role in message.server.roles:
                            if language in role.name:
                                characters.setLanguages(character, role)
                                await client.send_message(message.channel, characters.getName(character) + " now knows " + language[9:])
                                print("Adding", message.author, "to", role)
                                await client.add_roles(message.author, role)
                                roleSet = 1
                                break
                        if roleSet == 0:
                            await client.send_message(message.channel, "Do you speak english in what?")

                    if message.content.startswith("!languages"):
                        for language in characters.getLanguages(character):
                            await client.send_message(message.channel, character + " knows " + str(language)[9:])

                    if message.content.startswith("!me"):
                        #Gets users active character info
                        await client.send_message(message.channel,
                                                  "Character Name: " + characters.characters[character].name)
                        await client.send_message(message.channel,
                                                  "Class: " + characters.characters[character].characterClass)
                        await client.send_message(message.channel,
                                                  "Level: " + str(characters.characters[character].level))
                        await client.send_message(message.channel,
                                                  "Health: " + str(characters.characters[character].currentHealth) + "/" + str(characters.characters[character].maxHealth))
                        await client.send_message(message.channel,
                                                  "Race: " + characters.characters[character].race)
                        await client.send_message(message.channel,
                                                  "Gold: " + str(characters.characters[character].gold))
                        for language in characters.getLanguages(character):
                            await client.send_message(message.channel, character + " knows " + str(language)[9:])

            # TODO Allow player to update character stats
            if message.content.lower().startswith("!newcharacter ") or message.content.lower().startswith("!newchar "):
                characterName = message.content.lower().replace("!newcharacter ", "").replace("!newchar ", "").capitalize()
                if characters.addCharacter(characterName, message.author):
                    print("Created", characterName)
                    await client.send_message(message.channel, characterName + " has risen.")
                else:
                    await client.send_message(message.channel, characterName + " was already made.")

            if message.content.startswith("!active "):
                characterName = message.content.replace("!active ", "")
                if characters.setActive(characterName, message.author):
                    #TODO does not properly remove roles from user the first time, it works after switching back and forth a couple times

                    # remove user from all language roles
                    for role in message.server.roles:
                        if str(role).startswith("language_"):
                            print("removing", message.author, "from", role)
                            await client.remove_roles(message.author, role)

                    await client.send_message(message.channel, characterName + " is now active.")

                    # Add user to the languages for that active character
                    for language in characters.getLanguages(characterName):
                        print("Adding", message.author, "to", role)
                        await client.add_roles(message.author, language)
                else:
                    await client.send_message(message.channel, characterName + " could not be set as active")

            if message.content.startswith("!characters"):
                user = message.author
                # shows all the characters that are owned by a user
                name = str(user)
                for character in characters.getCharacters(user):
                    await client.send_message(message.channel, name + " owns " + character)

    # everyone commands
    if message.content.startswith("!help"):
        helpDM = "DM Commands\n"
        helpDM += "!registerLanguage language_name \n\t- Adds a language channel, users must know this language in order to join this voice channel\n"
        helpDM += "!deleteLanguage language_name \n\t- Removes language channel and roles associated to that language\n"
        helpPlayer = "Player Commands\n"
        helpPlayer += "!iknow language_name \n\t- Adds your player to the language role\n"
        output = helpDM + helpPlayer
        await client.send_message(message.channel, output)



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
        roleDM = None
        rolePlayer = None
        for role in server.roles:
            if role.name == "DM":
                roleDM = role
                hasDM = True
            elif role.name == "Player":
                rolePlayer = role
                hasPlayer = True
        if hasDM == False:
            roleDM = await client.create_role(server, name="DM")
        if hasPlayer == False:
            rolePlayer = await client.create_role(server, name="Player")
        # now that the roles exist give the DM role to the creator of the sever, and player to all other members
        for member in client.get_all_members():
            if member.server_permissions.administrator:
                await client.add_roles(member, roleDM)
            else:
                await client.add_roles(member, rolePlayer)
client.run(TOKEN)
