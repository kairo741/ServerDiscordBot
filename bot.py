from asyncio import sleep
from random import choice
from os import environ
from datetime import datetime
import discord
from discord.ext import commands
from mcstatus import JavaServer

client = commands.Bot(command_prefix=commands.when_mentioned_or("❒"), intents=discord.Intents.all(), help_command=None)
server_port = input("Qual a porta do server? ")
if server_port == "":
    server_port = "26262"
server = JavaServer.lookup(f"localhost:{server_port}")
server_init_time = datetime.now()

status = server.status()
onPlayers = status.players.online
maxPlayers = status.players.max


@client.event
async def on_ready():
    await sync_slash_commands()
    await send_is_online_message()
    await update_presence_while()


async def send_is_online_message():
    server_embed = discord.Embed(title="❒ Superidolඞ Server ❒",
                                 colour=discord.Colour.dark_green(),
                                 description="""```⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️
⬛️📗📗📗📗📗📗📗📗⬛️
⬛️📗📗📗📗📗📗📗📗⬛️
⬛️📗⬛️⬛️📗📗⬛️⬛️📗⬛️
⬛️📗⬛️⬛️📗📗⬛️⬛️📗⬛️
⬛️📗📗📗⬛️⬛️📗📗📗⬛️
⬛️📗📗⬛️⬛️⬛️⬛️📗📗⬛️
⬛️📗📗⬛️⬛️⬛️⬛️📗📗⬛️
⬛️📗📗⬛️📗📗⬛️📗📗⬛️
⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️
❒❒ ඞ 🅂🄴🅁🅅🄴🅁 🄾🄽 ඞ ❒❒```""")

    server_embed.add_field(name="🚪 | Porta", value=server_port, inline=True)
    server_embed.add_field(name="🛡️ | Radmin info", value="❒radmin", inline=True)

    server_embed.add_field(name='', value='', inline=False)

    server_embed.add_field(name="ℹ️ | Info geral", value="❒info", inline=True)
    server_embed.add_field(name="📙 | Comandos", value="❒help", inline=True)
    # channel = client.get_channel(967174674381410376)  # Canal de teste
    channel = client.get_channel(789557217698381824)  # Canal server boomers
    await channel.send(embed=server_embed)


async def sync_slash_commands():
    try:
        synced = await client.tree.sync()
        print(f'{len(synced)} slash commands foram sincronizados')
    except Exception as e:
        print(e)


async def update_presence_while():
    while True:
        await sleep(30)
        update_info()
        await client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(
                name=f"{onPlayers}/{maxPlayers} Players ❒Superidolඞ Server❒"))


def update_info():
    global status
    global onPlayers
    global maxPlayers
    status = server.status()
    onPlayers = status.players.online
    # print(onPlayers)
    maxPlayers = status.players.max
    # print(maxPlayers)


@client.hybrid_command(name="info", with_app_command=True, description="Mostra todas as informações do server ඞ")
async def update_presence(context):
    title_embed = discord.Embed(
        title="⛏🧱 Server Infos ⛏🧱",
        description="Veja as infos do servidor!",
        colour=discord.Colour.dark_gold(),
    )
    title_embed.set_thumbnail(
        url="https://feedback.minecraft.net/hc/article_attachments/6614151800461/Minecraft_WildUpdate_1920x1080.png")

    await context.send(embed=title_embed)
    await radmin_info_command(context)
    await server_info_command(context)
    await players_command(context)
    await time_info_command(context)


@client.hybrid_command(name="server", with_app_command=True, description="Mostra as informações do server")
async def server_info_command(context):
    message = discord.Embed(title="❒ Superidolඞ Server ❒",
                            colour=discord.Colour.green())
    message.add_field(name="Porta", value=server_port, inline=True)
    message.add_field(name="Versão",
                      value=f'Minecraft™ Java {status.version.name}',
                      inline=True)
    # Pular uma linha
    message.add_field(name='',
                      value='',
                      inline=False)
    message.add_field(name="👤 | Players Online",
                      value=status.players.online,
                      inline=True)
    message.add_field(name="👤 | Máximo de Players",
                      value=status.players.max,
                      inline=True)
    await context.send(embed=message)


@client.hybrid_command(name="time", with_app_command=True, description="Mostra o tempo online do server")
async def time_info_command(context):
    message = discord.Embed(title="⌛ Tempo online ⌛",
                            colour=discord.Colour.dark_teal())
    message.add_field(name="Iniciou-se", value=server_init_time.strftime("%d/%m/%Y %H:%M:%S"))
    message.add_field(name="Online à", value=str(datetime.now() - server_init_time).split('.')[0])
    # message.add_field(name="Online à", value=str(datetime.now() - server_init_time).split('.')[0]) # sem os milésimos
    await context.send(embed=message)


@client.hybrid_command(name="radmin", with_app_command=True, description="Mostra as informações da rede do radmin")
async def radmin_info_command(context):
    message = discord.Embed(title="🛡️ Radmin 🛡️",
                            colour=discord.Colour.dark_blue())
    message.add_field(name="Ip", value="26.72.211.149")
    message.add_field(name="Nome da Rede",
                      value="superidolඞ",
                      inline=False)
    message.add_field(name="Senha", value="123456", inline=False)
    await context.send(embed=message)


@client.hybrid_command(name="players", with_app_command=True, description="Mostra os players online do servidor")
async def players_command(context):
    players = ""
    for player in status.players.sample:
        players += f' ■ {player.name}\n'

    message = discord.Embed(
        title="👥 | Players online:",
        description=players if players != "" else "Nenhum player online!",
        colour=discord.Colour.purple())
    await context.send(embed=message)


@client.hybrid_command(name="update", with_app_command=True, description="Atualizar manualmente o status do bot")
async def update_command(context):
    update_info()

    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            name=f"❒Superidolඞ Server❒  {onPlayers}/{maxPlayers} Players"))
    message = discord.Embed(
        title="Status atualizado!",
        description="Status do bot com os players onlines, atualizado!",
        colour=discord.Colour.dark_green())
    await context.send(embed=message)


@client.hybrid_command(name="help", with_app_command=True, description="Lista todos os comandos do bot",
                       aliases=['commands', 'bot'])
async def help_command(context):
    message = discord.Embed(
        title="📙 | Comandos do bot",
        description="O prefixo para todos os comandos é: ❒\n Mas, o bot também conta com 'slash commands'",
        colour=discord.Colour.orange())

    for command in client.commands:
        message.add_field(name=f"❒{command.name}", value=command.description, inline=True)

    message.set_footer(text="Autor Kairo Amorim. https://github.com/kairo741",
                       icon_url='https://cdn.icon-icons.com/icons2/2699/PNG/512/minecraft_logo_icon_168974.png')

    await context.send(embed=message)


@client.hybrid_command(name="play", with_app_command=True, description="Toca músicas de fundo da versão 1.18")
async def play_music_with_bg(context):
    version = choice(["1.19", "1.18"])

    await sleep(5)
    message = discord.Embed()
    message.set_image(url=get_random_image())
    message.title = f"Tocando soundtrack da versão {version}"
    if version == "1.18":
        message.set_thumbnail(
            url='https://feedback.minecraft.net/hc/article_attachments/4414284675853/patchnotes_cavesandcliffs.jpg')
    else:
        message.set_thumbnail(
            url="https://feedback.minecraft.net/hc/article_attachments/6614151800461/Minecraft_WildUpdate_1920x1080.png")

    await context.send(embed=message)
    await play_sound(f"files/{version}_soundtrack.mp3", context)


async def play_sound(file_name, context):
    connect = True
    connected_channel = discord.utils.get(client.voice_clients, guild=context.guild)

    if connected_channel is None:
        connect = await join_channel(context)

    if connect:
        channel = discord.utils.get(client.voice_clients, guild=context.guild)
        channel.play(
            discord.FFmpegPCMAudio(executable="C:/path/ffmpeg.exe",
                                   source=file_name))
        return True


async def join_channel(context):
    author_voice = context.message.author.voice
    if author_voice is not None:
        await author_voice.channel.connect()
        return True
    else:
        return False


@client.hybrid_command(name="leave", with_app_command=True, description="Sai do chat de voz")
async def disconnect(context):
    channel = discord.utils.get(client.voice_clients, guild=context.guild)
    if channel is not None:
        await channel.disconnect(force=True)


@client.hybrid_command(name="stop", with_app_command=True, description="Para o som que estiver tocando no chat de voz")
async def stop_playing(context):
    channel = discord.utils.get(client.voice_clients, guild=context.guild)
    if channel is not None:
        channel.stop()


def get_random_image():
    images = [
        "https://preview.redd.it/g9rf0qn4drn61.png?width=2560&format=png&auto=webp&s"
        "=9df568e80f7e0262be26c58e765c0eab7d9a1e81",
        "https://preview.redd.it/jrasamn4drn61.png?width=2560&format=png&auto=webp&s"
        "=e2f949dad5bb0307cf3e85dc40697315aa076157",
        "https://preview.redd.it/ym3mpqn4drn61.png?width=2560&format=png&auto=webp&s"
        "=035bfba0db5fde1a767474b13ea52594af52b268",
        "https://preview.redd.it/bx98hon4drn61.png?width=2560&format=png&auto=webp&s"
        "=23381294aa57cc7b141d296111a77f3c06503858",
        "https://cdn.discordapp.com/attachments/868197064092295169/1063677102857146428/image.png",
        "https://cdn.discordapp.com/attachments/868197064092295169/1063677605481545808/image.png",
        "https://i.pinimg.com/originals/9c/f5/b6/9cf5b64d6cd2963ef96eabb4b2c1cbe6.jpg",
        "https://cdn.wallpapersafari.com/66/87/soOkrM.jpg"
    ]
    return choice(images)


client.run(environ["BOT_TOKEN"])
