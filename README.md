Joaquin MIRAVET
6°11°

Servidor.py

Importación de librerías

import socket
import threading
import requests

Explicacion:

Se importan las librerías necesarias para el funcionamiento del servidor. socket permite establecer la comunicación mediante el protocolo TCP/IP, threading posibilita atender varios clientes de forma simultánea mediante hilos de ejecución y requests se utiliza para realizar consultas HTTP a una API pública, incorporando información externa al chat.

Configuración del servidor

HOST = "0.0.0.0"
PORT = 5000
clientes = []
usuarios = {}

Explicacion:

Se define la dirección IP y el puerto donde el servidor escuchará las conexiones entrantes. La dirección 0.0.0.0 indica que aceptará conexiones desde cualquier interfaz de red disponible. Además, se inicializan dos estructuras de datos: una lista para almacenar todos los clientes conectados y un diccionario que relaciona cada socket con el nickname del usuario correspondiente.

Función broadcast()

def broadcast(mensaje, remitente):
for cliente in clientes:
if cliente != remitente:
try:
cliente.send(mensaje.encode('utf-8'))
except:
pass

Explicacion:

Esta función implementa el envío masivo de mensajes (broadcast). Recorre la lista de clientes conectados y envía el mensaje a todos ellos, excepto al cliente que lo originó. Antes del envío, el mensaje se convierte a bytes mediante encode(), ya que los sockets únicamente transmiten datos binarios. Si algún cliente presenta un error durante el envío, la excepción es ignorada para evitar que el servidor deje de funcionar.

Inicio de la función manejar_cliente()

def manejar_cliente(cliente):
try:
cliente.send("Ingrese su nickname: ".encode('utf-8'))
nickname = cliente.recv(1024).decode('utf-8')
usuarios[cliente] = nickname

Explicacion:

Esta función administra toda la comunicación con un cliente específico. Al conectarse, el servidor solicita un nickname, recibe la respuesta mediante recv(), la convierte a texto utilizando decode() y almacena la asociación entre el socket del cliente y su nombre dentro del diccionario de usuarios. De esta forma el servidor podrá identificar posteriormente quién envía cada mensaje.

Notificación de conexión

print(f"{nickname} se ha conectado.")
broadcast(f"{nickname} se ha unido al chat.", cliente)

Explicacion:

Una vez autenticado el usuario, el servidor informa por consola que un nuevo cliente se ha conectado y comunica el evento al resto de los usuarios mediante la función broadcast(). Esto permite que todos conozcan cuándo un nuevo integrante ingresa al chat.

Recepción continua de mensajes

while True:
mensaje = cliente.recv(1024).decode('utf-8')

Explicacion:

El servidor permanece escuchando continuamente los mensajes enviados por ese cliente. El ciclo infinito mantiene la comunicación activa hasta que el usuario se desconecta. Cada mensaje recibido se convierte desde bytes a texto para poder procesarlo.

Detección de comandos

if mensaje.startswith("/"):

Explicacion:

Antes de procesar un mensaje, el servidor verifica si comienza con el carácter “/”. Esto permite distinguir entre un comando del sistema y un mensaje común del chat. Esta técnica simplifica la incorporación de nuevas funcionalidades sin interferir con la comunicación normal entre usuarios.

Comando /usuarios

if mensaje == "/usuarios":
lista = ", ".join(usuarios.values())
cliente.send(f"Usuarios conectados: {lista}".encode('utf-8'))

Explicacion:

Este comando obtiene todos los nicknames almacenados en el diccionario usuarios, los une en una única cadena utilizando join() y envía la lista únicamente al cliente que realizó la consulta.

Comando /api

elif mensaje == "/api":
respuesta = requests.get("[https://catfact.ninja/fact](https://catfact.ninja/fact)").json()
cliente.send(f"Dato curioso: {respuesta['fact']}".encode('utf-8'))

Explicacion:

Cuando el usuario ejecuta /api, el servidor realiza una petición HTTP mediante la librería requests a una API pública. La respuesta es recibida en formato JSON y convertida automáticamente en un diccionario de Python mediante .json(). Finalmente se extrae el valor asociado a la clave "fact" y se envía al cliente como respuesta.

Comando inexistente

else:
cliente.send("Comando no reconocido.".encode('utf-8'))

Explicacion:

Si el usuario escribe un comando que no está implementado, el servidor responde indicando que dicho comando no existe, evitando comportamientos inesperados.

Mensajes normales

else:
texto = f"{nickname}: {mensaje}"
print(texto)
broadcast(texto, cliente)

Explicacion:

Cuando el mensaje no corresponde a un comando, el servidor lo interpreta como un mensaje común del chat. Se agrega el nickname del remitente para identificarlo y posteriormente el mensaje es enviado al resto de los clientes conectados mediante la función broadcast().

Desconexión del cliente

finally:
if cliente in clientes: clientes.remove(cliente)
if cliente in usuarios:
nombre = usuarios[cliente]
del usuarios[cliente]
broadcast(f"{nombre} ha abandonado el chat.", cliente)
cliente.close()

Explicacion:

Este bloque se ejecuta siempre que el cliente finaliza la conexión o se produce un error. El servidor elimina el socket de la lista de clientes, elimina el nickname del diccionario de usuarios, informa al resto de los participantes que el usuario abandonó el chat y finalmente libera los recursos cerrando el socket mediante close().

Creación del servidor TCP

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

Explicacion:

Se crea un socket utilizando direcciones IPv4 (AF_INET) y el protocolo TCP (SOCK_STREAM). Posteriormente se asocia el socket al puerto definido mediante bind() y se coloca en estado de escucha con listen(), quedando preparado para aceptar conexiones entrantes.

Aceptación de nuevos clientes

while True:
cliente, direccion = servidor.accept()
clientes.append(cliente)
hilo = threading.Thread(target=manejar_cliente, args=(cliente,))
hilo.start()

Explicacion:

El servidor permanece esperando conexiones de manera indefinida. Cada vez que un cliente se conecta, accept() devuelve un nuevo socket exclusivo para esa comunicación. El cliente se almacena en la lista de conexiones activas y se crea un nuevo hilo mediante threading.Thread() que ejecutará la función manejar_cliente(). Gracias a esta técnica, múltiples usuarios pueden utilizar el chat simultáneamente sin bloquear el funcionamiento del servidor.

Cliente.py

Importación de librerías

import socket
import threading

Explicacion:

El cliente utiliza la librería socket para establecer la conexión con el servidor mediante TCP y threading para permitir el envío y la recepción de mensajes de forma simultánea.

Configuración de conexión

HOST = "127.0.0.1"
PORT = 5000

Explicacion:

Se define la dirección IP del servidor y el puerto al cual el cliente intentará conectarse. En este ejemplo se utiliza 127.0.0.1, correspondiente al localhost, lo que indica que servidor y cliente se ejecutan en la misma computadora.

Creación del socket cliente

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

Explicacion:

Se crea un socket TCP utilizando IPv4 y posteriormente se establece la conexión con el servidor mediante connect(). A partir de este momento ambos equipos pueden intercambiar información.

Función recibir()

def recibir():
while True:
try:
mensaje = cliente.recv(1024).decode('utf-8')
print(mensaje)

Explicacion:

Esta función permanece ejecutándose constantemente a la espera de mensajes enviados por el servidor. Cada mensaje recibido se convierte desde bytes a texto mediante decode() y posteriormente se muestra por pantalla.

Manejo de desconexiones

except:
print("Desconectado del servidor.")
cliente.close()
break

Explicacion:

Si ocurre un error durante la recepción de datos, el cliente informa que la conexión fue interrumpida, cierra el socket y finaliza el ciclo de recepción para evitar errores posteriores.

Función escribir()

def escribir():
while True:
try:
mensaje = input()
cliente.send(mensaje.encode('utf-8'))

Explicacion:

Esta función permite al usuario ingresar mensajes desde el teclado. Cada mensaje es convertido a bytes mediante encode() y enviado inmediatamente al servidor utilizando send(). El servidor será el encargado de decidir si se trata de un comando o de un mensaje común.

Creación de los hilos

hilo_recibir = threading.Thread(target=recibir)
hilo_recibir.start()
hilo_escribir = threading.Thread(target=escribir)
hilo_escribir.start()

Explicacion:

El cliente crea dos hilos independientes. Uno permanece escuchando continuamente los mensajes enviados por el servidor, mientras que el otro permite al usuario escribir nuevos mensajes. Gracias a esta separación, el cliente puede enviar y recibir información simultáneamente sin que una tarea bloquee a la otra.
