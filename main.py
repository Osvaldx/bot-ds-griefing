import discord
import discord.ext
import discord.ext.commands
from discord.ext import commands
from packages.bot_token import TOKEN_BOT
from packages.funciones import *

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

@bot.command("server")
async def info_serverMC(ctx,direccion: str = None):
    if(direccion == None): # Validamos que el usuario haya ingresado una IP o direccion de MC
        await ctx.send("**[ ! ]** *Ingrese una IP de MC*")
        return
    
    datos_sv_mc = consulta_api_server(direccion) #Consultamos a la API para obtener toda la informacion de la IP
    datos_ip_sv = consultar_info_ip(datos_sv_mc['ip_address'])
    icono = f"https://api.mcstatus.io/v2/icon/{direccion}" #Obtenemos el ICONO del servidor

    #Mensajes que van en el embed
    mensaje_uno = f"**IP:** {datos_sv_mc['ip_address']} \n**Puerto:** {datos_sv_mc['port']}"
    mensaje_dos = f"**Players:** {datos_sv_mc['players']['online']}**/**{datos_sv_mc['players']['max']} \n**Version:** {datos_sv_mc['version']['name_clean']}"
    mensaje_tres = f"**ASN:** AS{datos_ip_sv['network']['autonomous_system']['asn']} \n**Organización:** {datos_ip_sv['network']['autonomous_system']['organization']}"
    mensaje_motd = f"**MOTD**:\n```{datos_sv_mc['motd']['clean']}```"

    #Creamos el EMBED para enviar por discord con el formato
    embed=discord.Embed(title="⌈ ɪɴꜰᴏʀᴍᴀᴄɪᴏ́ɴ ᴅᴇʟ ꜱᴇʀᴠɪᴅᴏʀ ⌋", description=f"~𝗰𝗼𝗻𝘀𝘂𝗹𝘁𝗮@: {datos_sv_mc['host']}")
    embed.set_author(name="« SkullBOT | MC »", icon_url="https://media.discordapp.net/attachments/1213856557666795561/1342329848827482193/skullbot.jpg?ex=67b93d97&is=67b7ec17&hm=600b410ee73e715bc3bd8c85f27e0039427465b8edc82544d5f6754dd3d24a1c&=&format=webp&width=347&height=347")
    embed.set_thumbnail(url=icono)
    embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
    embed.add_field(name="",value=mensaje_uno, inline=True)
    embed.add_field(name="", value=mensaje_dos, inline=True)
    embed.add_field(name="", value=mensaje_tres, inline=False)
    embed.add_field(name="", value=mensaje_motd, inline=False)
    embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
    embed.set_footer(text="github.com/Osvaldx")
    await ctx.send(embed=embed)

@bot.command("nick")
async def info_nickMC():
    pass

bot.run(TOKEN_BOT)