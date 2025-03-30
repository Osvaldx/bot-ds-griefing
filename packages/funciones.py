import requests
import uuid
import hashlib
from html2image import Html2Image

api_informacion_ips = "https://ip.guide/"
api_minecraft_profile = "https://api.mojang.com/users/profiles/minecraft/"
api_server_datos = f"https://api.mcsrvstat.us/3/"

def consulta_api_server(direccion: str)-> dict | list:
    #Consultamos a la API
    response = requests.get(api_server_datos + direccion)
    datos = response.json() #Transformamos a JSON

    return datos

def consultar_info_ip(direccion: str)->dict | list:
    #Consultamos a la API
    response = requests.get(api_informacion_ips + direccion)
    datos = response.json() #Transformamos a JSON

    return datos

def generar_uuids_jugador(nickname: str)->dict:
    #Guardamos los datos en un diccionario
    uuids_jugador = {}

    formato_nick_offline = "OfflinePlayer:" + nickname #Formato para las UUID offline
    md5_hash = hashlib.md5(formato_nick_offline.encode(encoding="utf-8")).digest() #Hasheamos el nombre y lo pasamos a una array de 16 bytes
    uuid_offline = str(uuid.UUID(bytes=md5_hash, version=3)) #Lo convertimos a UUID V3
    uuids_jugador['OfflineUUID'] = uuid_offline #Lo agregamos al dict 

    #Consultamos a la API
    response = requests.get(api_minecraft_profile + nickname)
    datos = response.json() #Transformamos a JSON
    #Validamos que sea premium o no
    if(datos.get('id')):
        nueva_uuid = ""
        ubicaciones = [8,12,16,20]

        for i,char in enumerate(datos['id']):
            for num in ubicaciones:
                if(i == num):
                    nueva_uuid += "-"
            nueva_uuid += char
        
        uuids_jugador['PremiumUUID'] = nueva_uuid
     
    return uuids_jugador

def consultar_api_friends(uuid: str)->list:
    #Consultamos la api y transformamos los datos a JSON
    api_friends = f"https://api.namemc.com/profile/{uuid}/friends"
    response = requests.get(api_friends)
    datos = response.json()

    lista_friends = []
    #Si la lista esta vacia no tiene sentido agregar nombres
    if(datos != []):
        for linea in datos:
            lista_friends.append(linea['name'])

    return lista_friends

def esPremium(nickname: str)->bool:
    return True if requests.get(api_minecraft_profile + nickname).json().get('id') else False

def obtener_motd_server(ip_servidor: str)->None:
    ruta_chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    ruta_guardar_server = "C:\\Users\\osvql\\Desktop\\dev\\python\\bot-discord-griefing\\images"

    response = requests.get(api_server_datos + ip_servidor)
    datos = response.json()
    try:
        motd = datos['motd']['html']
        mensaje = ""
        if(len(motd) > 1):
            mensaje = f"{motd[0]}<br>{motd[1]}"
        else:
            mensaje = motd[0]
            if(motd[0] == "A Minecraft Server"):
                mensaje = f'<span style="color: #b8b8b8">{mensaje}</span>'
    except:
        mensaje = '<span style="color: #FF0000">HA OCURRIDO UN ERROR</span>'
        print("no paso")

    codigo_html = f"""<div style="
    display: block;
    text-align: center;
    justify-content: center;
    align-content: center;
    color: var(--color-white);
    background-color: #0F0F0F;
    border-radius: 0.25rem;
    overflow-x: auto;
    width: 470px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;  
    font-feature-settings: normal;  
    font-variation-settings: normal;
    font-size: 1em;
    box-sizing: border-box;
    border: 0 solid;
    margin: 0;
    padding: 15px;
    line-height: 1.5;
    -webkit-text-size-adjust: 100%;
    tab-size: 4;
    -webkit-tap-highlight-color: transparent;">{mensaje}</div>"""

    hti = Html2Image(browser_executable=ruta_chrome,size=(1920,1080),output_path=ruta_guardar_server)
    hti.screenshot(html_str=codigo_html, save_as=f"server.png",size=(470,78))

def validar_numeros(numero: str)->bool:
    validado = False

    if(numero.isnumeric()):
        n = int(numero)
        if(n >= 0 and n <= 255):
            validado = True

    return validado

def validar_consulta_ips(ip_ingresada: str)->bool:
    if(ip_ingresada.count(".") == 3): # verificamos que sea una IPv4
        partes = ip_ingresada.split(":") # separamos el puerto si existe
        ip = partes[0].split(".") # separamos los numeros
        # Validamos que los numeros de las IP esten en el rango
        for num in ip:
            if(not validar_numeros(num)):
                return False # en caso de no estar en el rango o no ser un numero false
        # Validamos que el puerto sea numerico
        valido = False if(len(partes) == 2 and not partes[1].isnumeric()) else True
        
        return valido
    
    if(ip_ingresada.count(".")):
        if(all(char.isalnum() or char in ".-" for char in ip_ingresada)):
            return True
            
    return False

def validar_nicks(nickname:str)->bool:
    validado = False
    if(len(nickname) <= 16):
        validado = True if(char.isalnum() or char in "_" for char in nickname) else False
    
    return validado