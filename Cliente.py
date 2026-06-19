import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

cliente.connect((HOST, PORT))


def recibir():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')

            print(mensaje)

        except:
            print("Desconectado del servidor.")
            cliente.close()
            break


def escribir():
    while True:
        try:
            mensaje = input()
            cliente.send(mensaje.encode('utf-8'))

        except:
            cliente.close()
            break


hilo_recibir = threading.Thread(target=recibir)
hilo_recibir.start()

hilo_escribir = threading.Thread(target=escribir)
hilo_escribir.start()