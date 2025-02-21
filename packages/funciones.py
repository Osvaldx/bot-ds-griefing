import requests

api_server_java = "https://api.mcstatus.io/v2/status/java/"

def obtener_info(direccion: str):
    response = requests.get(api_server_java + direccion)
    data = response.json()
    print(data["host"])

obtener_info("mc.universocraft.com")