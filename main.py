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
    
    obtener_motd_server(direccion)
    datos_sv_mc = consulta_api_server(direccion) #Consultamos a la API para obtener toda la informacion de la IP
    datos_ip_sv = consultar_info_ip(datos_sv_mc['ip'])
    icono = f"https://api.mcstatus.io/v2/icon/{direccion}" #Obtenemos el ICONO del servidor

    #Mensajes que van en el embed
    mensaje_uno = f"<:punto:1343667939957800960> **IP:** {datos_sv_mc['ip']} \n<:punto:1343667939957800960> **Puerto:** {datos_sv_mc['port']}"
    mensaje_dos = f"<:punto:1343667939957800960> **Players:** {datos_sv_mc['players']['online']}**/**{datos_sv_mc['players']['max']} \n<:punto:1343667939957800960> **Protocolo:** {datos_sv_mc['protocol']['version']}"
    mensaje_tres = f"<:punto:1343667939957800960> **ASN:** AS{datos_ip_sv['network']['autonomous_system']['asn']} \n<:punto:1343667939957800960> **Organización:** {datos_ip_sv['network']['autonomous_system']['organization']}"
    mensaje_cuatro = f"<:punto:1343667939957800960> **Estado:** {'[<:online:1343663213862064128>] ᴏɴ' if {datos_sv_mc['online']} else '[<:offline:1343663227380301895>] ᴏꜰꜰ'}\n <:punto:1343667939957800960> **Version:** {datos_sv_mc['version']}"

    image_file = discord.File(f"server.png", filename=f"server.png")
    #Creamos el EMBED para enviar por discord con el formato
    embed=discord.Embed(title="⌈ ɪɴꜰᴏʀᴍᴀᴄɪᴏ́ɴ ᴅᴇʟ ꜱᴇʀᴠɪᴅᴏʀ ⌋", description=f"<:flecha:1343663258388922440> 𝗰𝗼𝗻𝘀𝘂𝗹𝘁𝗮@: {datos_sv_mc['hostname'] if datos_sv_mc.get('hostname') else direccion}")
    embed.set_author(name="« SkullBOT | MC »", icon_url="https://media.discordapp.net/attachments/1213856557666795561/1342329848827482193/skullbot.jpg?ex=67b93d97&is=67b7ec17&hm=600b410ee73e715bc3bd8c85f27e0039427465b8edc82544d5f6754dd3d24a1c&=&format=webp&width=347&height=347")
    embed.set_thumbnail(url=icono)
    embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
    embed.add_field(name="",value=mensaje_uno, inline=True)
    embed.add_field(name="", value=mensaje_dos, inline=True)
    embed.add_field(name="", value=mensaje_tres, inline=False)
    embed.add_field(name="", value=mensaje_cuatro, inline=True)
    # embed.add_field(name="", value=mensaje_motd, inline=False)
    embed.set_image(url=f"attachment://server.png")
    embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
    embed.set_footer(text="github.com/Osvaldx")
    await ctx.send(embed=embed, file=image_file)

@bot.command("nick")
async def info_nickMC(ctx, nickname: str = None):
    if(nickname == None): # Validamos que el usuario haya ingresado una IP o direccion de MC
        await ctx.send("**[ ! ]** *Ingrese el NICK de un jugador*")
        return

    datos_jugador = generar_uuids_jugador(nickname)
    mensaje_embed = f"<:flecha:1343663258388922440> **UUID ⌈ <:X_:1343663199198773298> ɴᴏ ᴘʀᴇᴍɪᴜᴍ ⌋:**```{datos_jugador['OfflineUUID']}```"
    skin = f"https://mc-heads.net/body/{nickname}"
    cabeza = f"https://mc-heads.net/avatar/{nickname}"

    #Si es PREMIUM le agregamos la UUID primero
    if(len(datos_jugador) > 1):
        mensaje_embed = f"<:flecha:1343663258388922440> **UUID ⌈ <:tilde:1343663175308152843> ᴘʀᴇᴍɪᴜᴍ ⌋:** ```{datos_jugador['PremiumUUID']}```\n" + mensaje_embed
    
    embed=discord.Embed(title="⌈ ɪɴꜰᴏʀᴍᴀᴄɪᴏ́ɴ ᴅᴇʟ ᴊᴜɢᴀᴅᴏʀ ⌋", description=f"<:flecha:1343663258388922440> 𝗷𝘂𝗴𝗮𝗱𝗼𝗿@: {nickname} <:candado:1343663244770021376>",color=0xAAAAAA)
    embed.set_author(name="« SkullBOT | MC »", icon_url="https://media.discordapp.net/attachments/1213856557666795561/1342329848827482193/skullbot.jpg?ex=67b93d97&is=67b7ec17&hm=600b410ee73e715bc3bd8c85f27e0039427465b8edc82544d5f6754dd3d24a1c&=&format=webp&width=347&height=347")
    embed.set_thumbnail(url=cabeza)
    embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
    embed.add_field(name="",value=mensaje_embed, inline=True)
    embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
    embed.set_image(url=skin)
    embed.set_footer(text="github.com/Osvaldx")
    await ctx.send(embed=embed)
    # if(jugador_premium):
    
@bot.command("friends")
async def info_friends(ctx, nickname: str = None):
    if(nickname == None): # Validamos que el usuario haya ingresado una IP o direccion de MC
        await ctx.send("**[ ! ]** *Ingrese el NICK de un jugador*")
        return
    
    if(esPremium(nickname)):
        datos_jugador = generar_uuids_jugador(nickname)
        lista_friends = consultar_api_friends(datos_jugador["PremiumUUID"])
        if(lista_friends != []):
            for jugador in lista_friends:
                cabeza_amigo = f"https://mc-heads.net/avatar/{jugador}"
                mensaje_embed_friend = f"<:flecha:1343663258388922440> **NICK:** {jugador if(jugador.count('_') < 1) else f'```{jugador}```'}\n<:flecha:1343663258388922440> **UUID ⌈ <:tilde:1343663175308152843> ᴘʀᴇᴍɪᴜᴍ ⌋:** ```{datos_jugador['PremiumUUID']}```"

                embed_friend=discord.Embed(title="⌈ ʟɪꜱᴛᴀ ᴅᴇ ᴀᴍɪɢᴏꜱ ⌋", description=f"<:flecha:1343663258388922440> 𝗮𝗺𝗶𝗴𝗼 𝗱𝗲 @: {nickname} <:candado:1343663244770021376>",color=0xAAAAAA)
                embed_friend.set_author(name="« SkullBOT | MC »", icon_url="https://media.discordapp.net/attachments/1213856557666795561/1342329848827482193/skullbot.jpg?ex=67b93d97&is=67b7ec17&hm=600b410ee73e715bc3bd8c85f27e0039427465b8edc82544d5f6754dd3d24a1c&=&format=webp&width=347&height=347")
                embed_friend.set_thumbnail(url=cabeza_amigo)
                embed_friend.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
                embed_friend.add_field(name="",value=mensaje_embed_friend, inline=False)
                embed_friend.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
                embed_friend.set_footer(text="github.com/Osvaldx")
                await ctx.send(embed=embed_friend)
        else:
            await ctx.send(f"**[ ! ]** *el jugador: {nickname} no tiene una lista de amigos*")
    else:
        await ctx.send("**[ ! ]** *el Jugador ingresado es* ⌈ <:X_:1343663199198773298> ɴᴏ ᴘʀᴇᴍɪᴜᴍ ⌋")

bot.run(TOKEN_BOT)