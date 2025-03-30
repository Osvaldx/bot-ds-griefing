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

@bot.command(name="avatar")
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

@bot.command(name="server")
async def info_serverMC(ctx,*,direccion: str = None):
    estado_server = False
    jugadores_conectados = False

    if(not validar_consulta_ips(direccion) or direccion == None):# Validamos que el usuario haya ingresado una IP o direccion de MC
        await ctx.send("**[ ! ]** *Ingrese una IP de MC valida")
        return
    
    obtener_motd_server(direccion)
    datos_sv_mc = consulta_api_server(direccion) #Consultamos a la API para obtener toda la informacion de la IP
    icono = f"https://api.mcstatus.io/v2/icon/{direccion}" #Obtenemos el ICONO del servidor

    embed=discord.Embed(title="⌈ ɪɴꜰᴏʀᴍᴀᴄɪᴏ́ɴ ᴅᴇʟ ꜱᴇʀᴠɪᴅᴏʀ ⌋", description=f"<:flecha:1343663258388922440> 𝗰𝗼𝗻𝘀𝘂𝗹𝘁𝗮@: {datos_sv_mc['hostname'] if datos_sv_mc.get('hostname') else direccion}")
    embed.set_author(name="« SkullBOT | MC »", icon_url="https://media.discordapp.net/attachments/1213856557666795561/1342329848827482193/skullbot.jpg?ex=67b93d97&is=67b7ec17&hm=600b410ee73e715bc3bd8c85f27e0039427465b8edc82544d5f6754dd3d24a1c&=&format=webp&width=347&height=347")
    embed.set_thumbnail(url=icono)
    embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
    image_file = discord.File(f"images/server.png", filename=f"server.png")
    datos_ip_sv = consultar_info_ip(datos_sv_mc['ip'])

    if(datos_sv_mc.get('online')):
        estado_server = True
        #Mensajes que van en el embed
        mensaje_uno = f"<:punto:1343667939957800960> **IP:** {datos_sv_mc['ip']} \n<:punto:1343667939957800960> **Puerto:** {datos_sv_mc['port']}"
        mensaje_dos = f"<:punto:1343667939957800960> **Players:** {datos_sv_mc['players']['online']}**/**{datos_sv_mc['players']['max']} \n<:punto:1343667939957800960> **Protocolo:** {datos_sv_mc['protocol']['version']}"
        mensaje_tres = f"<:punto:1343667939957800960> **ASN:** AS{datos_ip_sv['network']['autonomous_system']['asn']} \n<:punto:1343667939957800960> **Organización:** {datos_ip_sv['network']['autonomous_system']['organization']}"
        mensaje_cuatro = f"<:punto:1343667939957800960> **Estado:** {'[<:online:1343663213862064128>] ᴏɴ' if {datos_sv_mc['online']} else '[<:offline:1343663227380301895>] ᴏꜰꜰ'}\n <:punto:1343667939957800960> **Version:** {datos_sv_mc['version']}"


        if(datos_sv_mc.get('players').get('list')):
            await ctx.send("<a:cargando:1355769309783396402> - *Realizando consulta, puede llegar a demorar dependiendo la cantidad de conectados...*")
            jugadores_conectados = True
            lista_jugadores = datos_sv_mc.get('players').get('list')
            embed2=discord.Embed(title="⌈ ᴊᴜɢᴀᴅᴏʀᴇꜱ ᴄᴏɴᴇᴄᴛᴀᴅᴏꜱ ⌋", description=f"⌈<:alerta:1355761242542837881>⌋ *Las UUIDS se representan en el online-mode del servidor \n los usuarios pueden ser PREMIUM* ⌈<:alerta:1355761242542837881>⌋ \n• *Los jugadores PREMIUM tendran un <:tilde:1343663175308152843> al lado del nombre*")
            embed2.set_author(name="« SkullBOT | MC »", icon_url="https://media.discordapp.net/attachments/1213856557666795561/1342329848827482193/skullbot.jpg?ex=67b93d97&is=67b7ec17&hm=600b410ee73e715bc3bd8c85f27e0039427465b8edc82544d5f6754dd3d24a1c&=&format=webp&width=347&height=347")
            embed2.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
            for persona in lista_jugadores:
                if(len(embed2.fields) >= 25):
                    break
                datos_jugador = generar_uuids_jugador(persona.get('name'))
                jugador = f'```{persona.get("name")}```' if(persona.get('name').startswith('_') or persona.get('name').endswith('_')) else persona.get('name')
                tilde = f"<:tilde:1343663175308152843>\n" if(esPremium(jugador)) else f"\n"
                mensaje_embed_jugador = f'<:flecha:1343663258388922440> **NICK:** {jugador} {tilde} \n'
                if(persona.get('uuid') == datos_jugador.get('PremiumUUID')):
                    mensaje_embed2 = f"<:flecha:1343663258388922440> **UUID ⌈ <:tilde:1343663175308152843> ᴘʀᴇᴍɪᴜᴍ ⌋:** ```{datos_jugador.get('PremiumUUID')}```"
                elif(persona.get('uuid') == datos_jugador.get('OfflineUUID')):
                    mensaje_embed2 = f"<:flecha:1343663258388922440> **UUID ⌈ <:cruz:1343663199198773298> ɴᴏ ᴘʀᴇᴍɪᴜᴍ ⌋:** ```{datos_jugador.get('OfflineUUID')}```"
                elif(persona.get('name').startswith('.') or persona.get('name').startswith('BD_') or persona.get('name').endswith('_BD')):
                    mensaje_embed2 = f"<:flecha:1343663258388922440> **UUID ⌈ <:bedrock:1355771886730088558> ʙᴇᴅʀᴏᴄᴋ ⌋:** ```{persona.get('uuid')}```"
                else:
                    mensaje_embed2 = f"<:flecha:1343663258388922440> **UUID ⌈ <:custom:1355767708016181479> ᴄᴜꜱᴛᴏᴍ ⌋:** ```{persona.get('uuid')}```"
                embed2.add_field(name="",value=(mensaje_embed_jugador + mensaje_embed2), inline=False)
                embed2.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
            embed2.set_footer(text="github.com/Osvaldx")
    else:
        network = datos_ip_sv.get('network')
        autonomous_system = network.get('autonomous_system') if network.get('autonomous_system') else None

        mensaje_uno = f"<:punto:1343667939957800960> **IP:** {datos_sv_mc['ip']} \n<:punto:1343667939957800960> **Puerto:** {datos_sv_mc['port']}\n"
        mensaje_dos = f"<:punto:1343667939957800960> **EULA BLOCKED:** {'<:tilde:1343663175308152843>' if(datos_sv_mc.get('eula_blocked')) else '<:cruz:1343663199198773298>'}\n"
        mensaje_tres = f"<:punto:1343667939957800960> **ASN:** {'AS'+str(autonomous_system.get('asn')) if(autonomous_system) else 'No disponible'} \n<:punto:1343667939957800960> **Organización:** {autonomous_system.get('organization') if(autonomous_system) else 'No disponible'}"
        mensaje_cuatro = f"<:punto:1343667939957800960> **Estado:** {'[<:online:1343663213862064128>] ᴏɴ' if(datos_sv_mc['online']) else '[<:offline:1343663227380301895>] ᴏꜰꜰ'}"
    
    embed.add_field(name="",value=mensaje_uno, inline=True)
    embed.add_field(name="", value=mensaje_dos, inline=True)
    embed.add_field(name="", value=mensaje_tres, inline=False)
    embed.add_field(name="", value=mensaje_cuatro, inline=True)
    embed.set_image(url=f"attachment://server.png")
    embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value="", inline=False)
    embed.set_footer(text="github.com/Osvaldx")

    if(estado_server and jugadores_conectados):
        await ctx.send(embed=embed,file=image_file)
        await ctx.send(embed=embed2)
    elif(estado_server and not jugadores_conectados):
        await ctx.send(embed=embed,file=image_file)
    else:
        await ctx.send(embed=embed,file=image_file) # embed offline


@bot.command(name="nick")
async def info_nickMC(ctx, *,nickname: str = None):
    nickname = nickname.replace('"',"").replace("'","")
    if(nickname is None or not validar_nicks(nickname)): # Validamos que el usuario haya ingresado un nick correcto
        await ctx.send("**[ ! ]** *Ingrese el NICK de un jugador*")
        return

    datos_jugador = generar_uuids_jugador(nickname)
    mensaje_embed = f"<:flecha:1343663258388922440> **UUID ⌈ <:cruz:1343663199198773298> ɴᴏ ᴘʀᴇᴍɪᴜᴍ ⌋:**```{datos_jugador['OfflineUUID']}```"
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

@bot.command(name="friends")
async def info_friends(ctx, *,nickname: str = None):
    nickname = nickname.replace('"',"").replace("'","")
    if(nickname is None or not (validar_nicks(nickname))): # Validamos que el usuario haya ingresado una IP o direccion de MC
        await ctx.send("**[ ! ]** *Ingrese el NICK de un jugador*")
        return
    
    if(esPremium(nickname)):
        datos_jugador = generar_uuids_jugador(nickname)
        lista_friends = consultar_api_friends(datos_jugador["PremiumUUID"])
        if(lista_friends != []):
            for jugador in lista_friends:
                cabeza_amigo = f"https://mc-heads.net/avatar/{jugador}"
                mensaje_embed_friend = f"<:flecha:1343663258388922440> **NICK:** {f'```{jugador}```' if(jugador.startswith('_') or jugador.endswith('_')) else jugador}\n<:flecha:1343663258388922440> **UUID ⌈ <:tilde:1343663175308152843> ᴘʀᴇᴍɪᴜᴍ ⌋:** ```{datos_jugador['PremiumUUID']}```"

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
        await ctx.send("**[ ! ]** *el Jugador ingresado es* ⌈ <:cruz:1343663199198773298> ɴᴏ ᴘʀᴇᴍɪᴜᴍ ⌋")

bot.run(TOKEN_BOT)