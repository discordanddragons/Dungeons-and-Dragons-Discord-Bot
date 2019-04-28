# Work with Python 3.6
import discord
from discord.ext import commands
from random import randint
import re
import json

from characterManager import characterManager
from characterManager import Utility
TOKEN = 'NTYzMDUxMTA2ODkzMDM3NTk4.XKTzBA.kCuGuv8Onok8NZZm1Q5TfPfrGAc'

# TODO Still need to do some role stuff to make sure people can't join things that they shouldn't be able to

prefix = "!"
client = commands.Bot(command_prefix=prefix, case_insensitive=True)

# This is a list of the skills for the rolls
skillsDictRoll = {}
with open('./json/mechanics.json', encoding="utf8") as file:
    data = json.load(file)
    for key in data["Using Ability Scores"]["Ability Checks"]["Skills"]:
        if not key.startswith(tuple(["content", "Variant"])):
            skillsDictRoll[key] = [key]
            for skill in data["Using Ability Scores"]["Ability Checks"]["Skills"][key]:
                skillsDictRoll[key].append(skill)

    # print(skillsDictRoll)

# Character creation stuff
characters = characterManager()
utility = Utility()

@client.event
async def on_voice_state_update(before, after):
    isDM = False
    isPlayer = False
    for role in before.roles:
        if role.name == "DM":
            isDM = True
        elif role.name == "Player":
            isPlayer = True
    if before.guild_permissions.administrator or isDM:
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
    # TODO The DM is able to set the name of a game and players can join the game
    # TODO The DM is able to remove players from the game
    # TODO The DM is able to start the game
    print(message)
    await client.process_commands(message)



@client.event
async def on_member_join(member):
    for role in member.guild.roles:
        if role.name == "Player":
            await client.add_roles(member, role)


@client.event
async def on_ready():
    print("Everything's all ready to go~")
    for guild in client.guilds:
        # first ensure that the roles exist for DM and players
        hasDM = False
        hasPlayer = False
        hasActive = False

        roleDM = None
        rolePlayer = None
        for role in guild.roles:
            if role.name == "DM":
                roleDM = role
                hasDM = True
            if role.name == "Player":
                rolePlayer = role
                hasPlayer = True
            if role.name == "Active":
                hasActive = True

        if hasDM is False:
            roleDM = await guild.create_role(name="DM")

        if hasPlayer is False:
            rolePlayer = await guild.create_role(name="Player")

        if hasActive is False:
            await guild.create_role(name="Active")

        # now that the roles exist give the DM role to the creator of the sever, and player to all other members
        for member in client.get_all_members():
            if member.guild_permissions.administrator:
                await member.add_roles(roleDM)
            else:
                await member.add_roles(rolePlayer)


@client.command()
@commands.has_role('Player')
async def test(ctx, className):
    """Hey, go fuck yourself."""
    await ctx.send(className)


@test.error
async def test_error(ctx, error):
    await ctx.send('Youre not a fuckin player')


@client.command(pass_context=True, aliases=['newcharacter'])
async def newchar(ctx, characterName):
    """Creates a new character with the character name."""
    characterName = characterName.lower().capitalize()
    if characters.addCharacter(characterName, ctx.author):
        characters.setActive(characterName, ctx.author)
        role = discord.utils.get(ctx.guild.roles, name="Active")
        user = ctx.message.author
        await user.add_roles(role)
        await user.edit(nick=characterName)
        await ctx.send(characterName + " has risen and is active.")
    else:
        await ctx.send(characterName + " was already made.")


@client.command()
async def active(ctx, characterName):
    """Sets your character as the active one."""
    characterName = characterName.lower().lstrip().capitalize()
    if characters.setActive(characterName, ctx.author):
        # remove user from all language roles
        user = ctx.message.author
        for role in ctx.author.roles:
            if str(role).startswith("language_"):
                print("removing", ctx.author, "from", role)
                await user.remove_roles(ctx.author, role)

        await ctx.send(characterName + " is now active.")

        # Add user to the languages for that active character
        for language in characters.getLanguages(ctx.author):
            print("Adding", ctx.author, "to", role)
            await ctx.author.add_roles(language)
            user = ctx.message.author
            await user.edit(nick=characterName)
    else:
        await ctx.send(characterName + " could not be set as active")


@client.command()
async def iknow(ctx, language):
    """Adds a language to your character."""
    language = "language_" + language.lower()
    roleSet = 0
    for role in ctx.guild.roles:
        if language in role.name:
            character = characters.getActive(ctx.author)
            characters.setLanguages(ctx.author, role)
            message = "```" + character + " now knows " + language[9:] + "```"
            await ctx.send(message)
            print("Adding", ctx.author, "to", role)
            await ctx.author.add_roles(role)
            roleSet = 1
            break
    if roleSet == 0:
        await ctx.send(ctx.channel, "```Langauge does not exist```")


@client.command()
async def me(ctx):
    """Gets info about your character."""
    temp = characters.getCharacters(ctx.author)
    infoWars = "------------"
    for character in temp:
        infoWars += character
    print(infoWars)
    await ctx.author.send(infoWars)
    return



    user = ctx.author
    # shows all the characters that are owned by a user
    name = str(user)
    for character in characters.getCharacters(user):
        message = name + " owns " + character
        await ctx.author.send(message)


@client.command()
async def flip(ctx):
    """Flips a coin."""
    flip = utility.flip()
    print(flip)
    await ctx.send(flip)


@client.command(aliases=['r'])
async def roll(ctx, roll):
    if "d" in roll:
        dice = roll.lower()
        # print("dice:", dice)
        values = skillsDictRoll.values()
        # print(skills)

        if dice in [x for v in values for x in v if type(v) == list]:
            # print("Line 1")
            if characters.getActive(ctx.author):
                # get a dictionary of all the rolls the dm can ask you to d
                # print("print line3")

                for key, value in skillsDictRoll.items():
                    # print(key, value)
                    if dice in value:
                        stat = key
                print(stat)
                print(characters.roll(ctx.author, stat))
                # roll a d20 and add the appropriate modifier
                roll = utility.roll(1, 20)
                await ctx.send(str(roll[0]) + " add th e" + stat + " modifier pls =)")

                # characters.characters[character].getModifier(stat)

        else:
            diceSplit = re.findall(r"(\d+)d(\d+)", dice)
            rollNumber = int(diceSplit[0][0])
            diceSize = int(diceSplit[0][1])
            rolls = utility.roll(rollNumber, diceSize)

            if len(rolls) == 0:
                print("Please roll a number of dice between 1 and 100")
            else:
                rollResult = "```%s rolled:\n" % ctx.author
                for index, roll in enumerate(rolls):
                    # print("Roll #", index + 1, ":", roll)
                    rollResult += "Roll #" + str(index + 1) + ": " + str(roll) + "\n"
                rollResult += "```"
                await ctx.send(rollResult)


@client.command()
@commands.has_role(['Active'])
async def set(ctx, thing):
    # Allow the user to set whatever they want
    thing = thing.lower().split()
    if characters.getActive(ctx.author):
        character = characters.getActive(ctx.author)
        if len(thing) == 1:

            # The user is trying to use one of the prebuilt sets
            if thing[0] == "stats":
                introMsg = "How would you like to build your character?\n"
                introMsg += "Point Buy, Roll or Random?"
                await ctx.send(introMsg)

                def check(msg):
                    return msg.content.replace(" ", "").lower().startswith('pointbuy') \
                           or msg.content.replace(" ", "").lower().startswith('roll') \
                           or msg.content.replace(" ", "").lower().startswith('random')

                message = await client.wait_for_message(author=ctx.author, check=check)
                buildWith = message.content.replace(" ", "").lower()
                if buildWith.startswith('pointbuy'):
                    characters.characters[character].builtUsing = "pointbuy"
                    await ctx.send(message.channel,
                                              "Ok, building your character with the point buy System")

                if buildWith.startswith('roll'):
                    characters.characters[character].builtUsing = "roll"
                    await ctx.send(message.channel,
                                              "Ok, building your character by rolling for values")

                if buildWith.startswith('random'):
                    characters.characters[character].builtUsing = "random"
                    await ctx.send(message.channel,
                                              "Ok, randomly setting values for your character")
                    characters.setRandomStats(character)
                    statMessage = "Here are your character's Stats! Good luck!\n"
                    stats = characters.getStats(character)
                    for key, value in stats.items():
                        statMessage += key + ": " + str(value) + "\n"
                    await ctx.send(statMessage)

            if thing[0] == "race":
                await ctx.send("What race are you?")
                raceList = ["dwarf", "elf", "halfling", "human", "dragonborn",
                            "gnome", "half-elf", "half-orc", "tiefling"]

                def check(msg):
                    return msg.content.replace(" ", "").lower().startswith(tuple(raceList))

                message = await client.wait_for_message(author=message.author, check=check)

                race = message.content.replace(" ", "")
                characters.characters[character].gofuckyourself["race"] = race
                await ctx.send("You are now a " + race)

            if thing[0] == "class":
                await ctx.send("What class are you?")
                characterClassList = ["barbarian", "bard", "cleric", "druid", "fighter",
                                      "monk", "paladin", "ranger", "rogue", "sorcerer", "warlock",
                                      "wizard"]

                def check(msg):
                    return msg.content.replace(" ", "").lower().startswith(tuple(characterClassList))

                message = await client.wait_for_message(author=message.author, check=check)

                characterClass = message.content.replace(" ", "")
                characters.characters[character].gofuckyourself["characterClass"] = characterClass
                await ctx.send("You are now a " + characterClass)

                characters.setActive(character, message.author)

        if len(thing) == 2:
            # the user is trying to set a specific thing
            # !set strength 16
            characters.set(character, thing[0], thing[1])


@client.command(aliases=['al'])
@commands.has_role('DM')
async def addLanguage(ctx, language):
    for guild in client.guilds:
        print(guild)
        channelname = "language_" + language.replace("!registerLanguage ", "").lower()
        print(channelname)

        #Create a new voice channel
        await guild.create_voice_channel(channelname)

        #create a new role
        await guild.create_role(name=channelname)

        #set it so that noone can enter the channel
        channel = discord.utils.get(ctx.guild.channels, name=channelname)

        for role in guild.roles:
            await channel.set_permissions(role, connect=False)
        # if there is a reason to make chats hidden until joined then uncomment this
        # overwrite.read_messages = False


@client.command(aliases=['rl'])
@commands.has_role('DM')
async def removeLanguage(ctx, language):
    language = "language_" + language.replace("!registerLanguage ", "").lower()
    role = discord.utils.get(ctx.guild.roles, name=language)
    await role.delete()
    channel = discord.utils.get(ctx.guild.channels, name=language)
    await channel.delete()
    await ctx.send("Removed " + language)

# TODO DM can create a game
# TODO The game has a dictionary of all the players and the characters that they are playing
# TODO DM can show all games that is on the server and set a game to active
# TODO DM can kick players out of a game
# TODO DM can add players to a game
# TODO Players can join a game


client.run(TOKEN)
