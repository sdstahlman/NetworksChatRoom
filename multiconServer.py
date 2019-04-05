# Chat Room Project
#
#
# Olin Ballentine
# Josias Cruz
# Salma Hanafi
# Scott Stahlman
#
#

# Import Socket elements
from socket import AF_INET, socket, SOCK_STREAM

# Import Threading elements
from threading import Thread

# Importing date and time elements
import datetime

# Creating broadcast method to send a message to all connected clients
def broadcast(message, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + message)


# Method to search for incoming connections to the server
def acceptIncomingConn():
    while True:

        client, clientAddress = SERVER.accept()

        # Printing the connected client info once connection is established
        print("%s:%s connected." % clientAddress)

        client.send(bytes("Please enter your name, then press the 'Enter' key.", "utf8"))

        # Keeping track of the connected client addresses
        addresses[client] = clientAddress

        Thread(target=handleClient, args=(client,)).start()


# Method to define how each client is handled by the server (connections, disconnections, messages)
def handleClient(client):

    name = client.recv(BUFSIZ).decode("utf8")

    welcome = 'Welcome %s. Type #exit# to exit.' % name

    client.send(bytes(welcome, "utf8"))

    msg = "%s has connected." % name

    broadcast(bytes(msg, "utf8"))

    clients[client] = name

    while True:

        msg = client.recv(BUFSIZ)

        if msg != bytes("{quit}", "utf8"):
            # Getting current time
            currentDT = datetime.datetime.now()
            prefix = currentDT.strftime("%I:%M %p") + " | " + name + ": "
            broadcast(msg, prefix)

        else:
            client.send(bytes("#exit#", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has disconnected." % name, "utf8"))
            break


# Creating clients and addresses arrays to keep track of connected clients
clients = {}

addresses = {}

# Connection info for the Server
# NOTE: Client needs to know Host and Port Num to connect
HOST = '10.216.70.222'

PORT = 65432

SERVERADDR = (HOST, PORT)

BUFSIZ = 1024

SERVER = socket(AF_INET, SOCK_STREAM)

SERVER.bind(SERVERADDR)


# Listening and connecting to 5 clients
if __name__ == "__main__":
    SERVER.listen(5)

    print("Waiting.......")

    ACCEPT_THREAD = Thread(target=acceptIncomingConn)

    ACCEPT_THREAD.start()

    ACCEPT_THREAD.join()

    # Closing server once finished
    SERVER.close()
