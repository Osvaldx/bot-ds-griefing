import requests

api_server_java = "https://api.mcstatus.io/v2/status/java/"

def consulta_api_server(direccion: str)-> dict | list:
    response = requests.get(api_server_java + direccion)
    data = response.json()

    return data