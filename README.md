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

[image]  
**Ejemplo**: `$server 199.127.60.166:25666`

Este comando también se actualizará dinámicamente si el servidor tiene jugadores conectados en ese momento.

---

### 2. **$nick [nombre del usuario]**

Este comando te permite consultar información detallada sobre un jugador de Minecraft dado su nombre de usuario. A través de este comando, podrás obtener:

- **Estado Premium o No Premium** del jugador.
- **Skin del jugador** (una imagen visual del avatar).
- **UUID del jugador** en caso de ser Premium o No Premium.

**Ejemplo**: `$nick Notch`

Este comando es útil para conocer detalles adicionales sobre un jugador, incluyendo si es un usuario Premium o No Premium.

[image]  

---

### 3. **$friends [nombre del usuario]**

Este comando te permite ver la lista de amigos de un usuario de Minecraft. Con este comando, puedes obtener:

- **Lista de amigos del jugador**
- **UUIDs de los amigos** (si están disponibles)

**Ejemplo**: `$friends skquery`

Este comando facilita el acceso a la red de jugadores conectados, ayudando a descubrir amigos o jugadores cercanos a un usuario específico.

[image]  

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
