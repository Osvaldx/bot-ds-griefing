import requests
import uuid
import hashlib

api_server_java = "https://api.mcstatus.io/v2/status/java/"
api_informacion_ips = "https://ip.guide/"
api_minecraft_profile = "https://api.mojang.com/users/profiles/minecraft/"

def consulta_api_server(direccion: str)-> dict | list:
    #Consultamos a la API
    response = requests.get(api_server_java + direccion)
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
        uuid_premium = datos['id']
        nueva_uuid = ""
        contador = 4
        activar_contador = False
        vueltas = 0

        #Con este for le damos formato de xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        for i in range(len(uuid_premium)):
            if(i == 8):
                nueva_uuid += "-"
                activar_contador = True
            
            if((contador == 0) and (vueltas < 3)):
                nueva_uuid += "-"
                contador = 4
                vueltas += 1

            nueva_uuid += uuid_premium[i]
            if(activar_contador):
                contador -= 1
        
        uuids_jugador['PremiumUUID'] = nueva_uuid
    
    return uuids_jugador
