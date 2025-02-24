import requests

api_server_java = "https://api.mcstatus.io/v2/status/java/"
api_informacion_ips = "https://ip.guide/"

def consulta_api_server(direccion: str)-> dict | list:
    response = requests.get(api_server_java + direccion)
    data = response.json()

    return data

def consultar_info_ip(direccion: str)->dict | list:
    response = requests.get(api_informacion_ips + direccion)
    data = response.json()

    return data