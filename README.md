# Minecraft Discord Bot

## Descripción del Proyecto

Este bot de Discord está diseñado para facilitar la interacción con servidores y jugadores de **Minecraft** dentro de un servidor de Discord. Ofrece varias funcionalidades que permiten obtener información detallada sobre servidores de Minecraft, usuarios, y sus conexiones. Todo esto a través de simples comandos que puedes utilizar para obtener datos como la IP del servidor, la versión de Minecraft, la lista de jugadores conectados, y detalles sobre los usuarios.

## Comandos del Bot

### 1. **$server [IP del servidor]**

Este comando te permite consultar información detallada sobre un servidor de Minecraft dado su IP y puerto. A través de este comando, podrás obtener:

- **IP del servidor**
- **Puerto**
- **Cantidad de usuarios conectados**
- **Dirección ASN**
- **Compañía**
- **Versión del servidor**
- **Estado del servidor (si está online o no)**
- **Protocolo**

**Ejemplo n°1**: `$server 199.127.60.166:25666`
![image](https://github.com/user-attachments/assets/dd6b4138-cf09-46f6-bff4-b076e2273404)
![image](https://github.com/user-attachments/assets/bba0c78b-71f3-4f1f-8326-7eb6fdc4fa47)

**Ejemplo n°2**: `$server mc.universocraft.com`
![image](https://github.com/user-attachments/assets/504d8a44-53d4-42b9-b1cb-69c04c7bb141)


Este comando también se actualizará dinámicamente si el servidor tiene jugadores conectados en ese momento.

---

### 2. **$nick [nombre del usuario]**

Este comando te permite consultar información detallada sobre un jugador de Minecraft dado su nombre de usuario. A través de este comando, podrás obtener:

- **Estado Premium o No Premium** del jugador.
- **Skin del jugador** (una imagen visual del avatar).
- **UUID del jugador** en caso de ser Premium o No Premium.

Este comando es útil para conocer detalles adicionales sobre un jugador, incluyendo si es un usuario Premium o No Premium.
**Ejemplo**: `$nick Rx5`
![image](https://github.com/user-attachments/assets/c1e71df0-b50b-4503-bd74-9a07a3cb4adb)

---

### 3. **$friends [nombre del usuario]**

Este comando te permite ver la lista de amigos de un usuario de Minecraft. Con este comando, puedes obtener:

- **Lista de amigos del jugador**
- **UUIDs de los amigos** (si están disponibles)
Este comando facilita el acceso a la red de jugadores conectados, ayudando a descubrir amigos o jugadores cercanos a un usuario específico.

**Ejemplo**: `$friends ipforwarding`
![image](https://github.com/user-attachments/assets/02e60d5e-ebcf-4419-8bfe-d95a79b7fc4e)

---

## Instalación
*Clona este repositorio:*
```bash
  git clone https://github.com/Osvaldx/bot-ds-griefing.git
```
*Navega al directorio del proyecto:*
```bash
  cd bot-ds-griefing
```
*Instala las dependencias:*
```bash
  pip install -r requirements.txt
```
*Como usarlo*
```bash
  python main.py
```

## Requisitos
- Python 3.8 o superior
- requests para realizar solicitudes HTTP
- uuid y hashlib para generar las UUIDs
- html2image==2.0.4 (importante que sea esta version)
- discord
---
