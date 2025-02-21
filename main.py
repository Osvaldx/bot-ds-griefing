import discord
import discord.ext
from discord.ext import commands
import discord.ext.commands
from packages.bot_token import TOKEN_BOT

intents = discord.Intents.default()

intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$",intents=intents)

@bot.event
async def on_ready():
    print(" "*5 + f"[+] BOT ENCENDIDO: {bot.user}")

@bot.command("avatar")
async def enviar_avatar(ctx,usuario: str = None):
    canal = ctx.channel # establecemos el canal donde estamos

    if(usuario is None): # validamos que si no se envio nada automaticamente sea None y asi remplazarlo por el autor
        usuario = ctx.author
    else:
        try: # intentamos convertir el mensaje a un Miembro
            usuario = await commands.MemberConverter().convert(ctx=ctx,argument=usuario)
        except: # en caso de q no sea un miembro se tira un mensaje de alerta
            await canal.send("**[!] No se encontro al usuario**")
            return

    await canal.send(usuario.avatar.url) # se envia la foto del usuario

@bot.command("info")
async def info_serverMC(ctx,direccion: str = None):
    embed=discord.Embed(title="⌈ ɪɴꜰᴏʀᴍᴀᴄɪᴏ́ɴ ᴅᴇʟ ꜱᴇʀᴠɪᴅᴏʀ ⌋", description="~@: mc.universocraft.com")
    embed.set_author(name="« SkullBOT | MC »", icon_url="https://media.discordapp.net/attachments/1213856557666795561/1342329848827482193/skullbot.jpg?ex=67b93d97&is=67b7ec17&hm=600b410ee73e715bc3bd8c85f27e0039427465b8edc82544d5f6754dd3d24a1c&=&format=webp&width=347&height=347")
    embed.set_thumbnail(url="https://api.mcstatus.io/v2/icon/mc.universocraft.com")
    embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="IP: {ip_sv}", inline=True)
    embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
    embed.set_footer(text="github.com/Osvaldx")
    await ctx.send(embed=embed)

bot.run(TOKEN_BOT)