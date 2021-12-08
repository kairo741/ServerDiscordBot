from asyncio import sleep
from random import randint

import discord
from discord.ext import commands
from mcstatus import MinecraftServer

client = commands.Bot(command_prefix="❒")
serverPort = input("Qual a porta do server? ")
server = MinecraftServer.lookup(f"localhost:{serverPort}")

status = server.status()
onPlayers = status.players.online
maxPlayers = status.players.max


@client.event
async def on_ready():
    serverEmbed = discord.Embed(title="❒ Superidolඞ Server ❒",
                                description="""
:green_circle: :green_circle::green_circle::green_circle::green_circle:  :green_circle:
:green_circle:ඞ❒ඞ❒ඞ❒ඞ:green_circle:
:green_circle:❒Server On❒ :green_circle:
:green_circle:ඞ❒ඞ❒ඞ❒ඞ:green_circle:
:green_circle: :green_circle::green_circle::green_circle::green_circle:  :green_circle:
		""",
                                colour=discord.Colour.dark_green())
    serverEmbed.add_field(name="Porta", value=serverPort, inline=True)
    serverEmbed.add_field(name="Radmin info", value="❒info", inline=True)
    channel = client.get_channel(789557217698381824)
    await channel.send(embed=serverEmbed)
    await updatePresenceWhile()


async def updatePresenceWhile():
    while (True):
        await sleep(30)
        updateInfo()
        await client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(
                name=f"{onPlayers}/{maxPlayers} Players ❒Superidolඞ Server❒"))


def updateInfo():
    global status
    global onPlayers
    global maxPlayers
    status = server.status()
    onPlayers = status.players.online
    # print(onPlayers)
    maxPlayers = status.players.max
    # print(maxPlayers)c


@client.command("info")
async def updatePresence(context):
    titleEmbed = discord.Embed(
        title="Server Infos",
        description="Veja as infos do servidor!",
        colour=discord.Colour.dark_gold(),
    )
    titleEmbed.set_thumbnail(
        url="https://xboxplay.games/uploadStream/23781.jpg")

    radminEmbed = discord.Embed(title="Radmin",
                                colour=discord.Colour.dark_blue())
    radminEmbed.add_field(name="Ip", value="26.72.211.149")
    radminEmbed.add_field(name="Nome da Rede",
                          value="superidolඞ",
                          inline=False)
    radminEmbed.add_field(name="Senha", value="123456", inline=False)

    serverEmbed = discord.Embed(title="❒ Superidolඞ Server ❒",
                                colour=discord.Colour.green())
    serverEmbed.add_field(name="Porta", value=serverPort, inline=False)
    serverEmbed.add_field(name="Players Online",
                          value=status.players.online,
                          inline=True)
    serverEmbed.add_field(name="Players Máximos",
                          value=status.players.max,
                          inline=True)

    await context.send(embed=titleEmbed)
    await context.send(embed=radminEmbed)
    await context.send(embed=serverEmbed)


@client.command("update")
async def updateCommand(context):

    updateInfo()

    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            name=f"❒Superidolඞ Server❒  {onPlayers}/{maxPlayers} Players"))
    message = discord.Embed(
        title="Status atualizado!",
        description="Status do bot com os players onlines, atualizado!",
        colour=discord.Colour.dark_green())
    await context.send(embed=message)


@client.command("play")
async def playMusicWithBG(context):
    await sleep(5)
    message = discord.Embed()
    message.set_image(url=getRadomImage())
    await context.send(embed=message)
    played = await playSound("1.18_sounds.mp3", context)


async def playSound(fileName, context):
    connect = True
    connectedChannel = discord.utils.get(client.voice_clients,
                                         guild=context.guild)

    if connectedChannel == None:
        connect = await joinChannel(context)

    if connect:
        channel = discord.utils.get(client.voice_clients, guild=context.guild)
        channel.play(
            discord.FFmpegPCMAudio(executable="C:/path/ffmpeg.exe",
                                   source=fileName))
        return True


async def joinChannel(context):
    authorVoice = context.message.author.voice
    if authorVoice != None:
        await authorVoice.channel.connect()
        return True

    else:
        return False


def getRadomImage():
    imgs = [
        "https://preview.redd.it/g9rf0qn4drn61.png?width=2560&format=png&auto=webp&s=9df568e80f7e0262be26c58e765c0eab7d9a1e81",
        "https://preview.redd.it/jrasamn4drn61.png?width=2560&format=png&auto=webp&s=e2f949dad5bb0307cf3e85dc40697315aa076157",
        "https://preview.redd.it/ym3mpqn4drn61.png?width=2560&format=png&auto=webp&s=035bfba0db5fde1a767474b13ea52594af52b268",
        "https://preview.redd.it/bx98hon4drn61.png?width=2560&format=png&auto=webp&s=23381294aa57cc7b141d296111a77f3c06503858"
    ]
    return (imgs[randint(0, len(imgs) - 1)])

with open('token.txt') as f:
    token = f.read()
client.run(token)
