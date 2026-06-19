import socket
import threading
import requests

HOST = "0.0.0.0"
PORT = 5000

clientes = []
usuarios = {}


def broadcast(mensaje, remitente):
    for cliente in clientes:
        if cliente != remitente:
            try:
                cliente.send(mensaje.encode('utf-8'))
            except:
                pass


def manejar_cliente(cliente):
    try:
        cliente.send("Ingrese su nickname: ".encode('utf-8'))
        nickname = cliente.recv(1024).decode('utf-8')

        usuarios[cliente] = nickname

        print(f"{nickname} se ha conectado.")

        broadcast(f"{nickname} se ha unido al chat.", cliente)

        while True:
            mensaje = cliente.recv(1024).decode('utf-8')

            if mensaje.startswith("/"):

                if mensaje == "/usuarios":
                    lista = ", ".join(usuarios.values())
                    cliente.send(
                        f"Usuarios conectados: {lista}".encode('utf-8')
                    )

                elif mensaje == "/api":
                    try:
                        respuesta = requests.get(
                            "https://catfact.ninja/fact"
                        ).json()

                        cliente.send(
                            f"Dato curioso: {respuesta['fact']}".encode('utf-8')
                        )

                    except:
                        cliente.send(
                            "Error al consultar la API.".encode('utf-8')
                        )

                else:
                    cliente.send(
                        "Comando no reconocido.".encode('utf-8')
                    )

            else:
                texto = f"{nickname}: {mensaje}"
                print(texto)
                broadcast(texto, cliente)

    except:
        pass

    finally:
        if cliente in clientes:
            clientes.remove(cliente)

        if cliente in usuarios:
            nombre = usuarios[cliente]
            del usuarios[cliente]

            broadcast(
                f"{nombre} ha abandonado el chat.",
                cliente
            )

        cliente.close()


servidor = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

servidor.bind((HOST, PORT))
servidor.listen()

print(f"Servidor iniciado en puerto {PORT}")

while True:
    cliente, direccion = servidor.accept()

    print(f"Nueva conexión desde {direccion}")

    clientes.append(cliente)

    hilo = threading.Thread(
        target=manejar_cliente,
        args=(cliente,)
    )

    hilo.start()