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


# Creating broadcast method to send a message to all connected clients
def broadcast(message, prefix = ""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + message)


# Method to search for incoming connections to the server
def acceptIncomingConn():
    while True:

        client, clientAddress = SERVER.accept()

        # Printing the connected client info once connection is established
        print("%s:%s connected." %clientAddress)

        client.send(bytes("Please enter your name, then press the 'Enter' key.", "utf8"))

        # Keeping track of the connected client addresses
        addresses[client] = clientAddress

        Thread(target=handleClient, args=(client,)).start()


# Method to define how each client is handled by the server (connections, disconnections, messages)
def handleClient(client):

    # Storing client name for greeting
    clientName = client.recv(BUFSIZ).decode("utf8")

    welcomeMsg = "Welcome to the chat room, $s. To exit the room, please type #exit#." %clientName

    # Greeting message displayed to client
    client.send(bytes(welcomeMsg, "utf8"))

    chatJoinMsg = "%s has joined." %clientName

    # Sending 'user joined' message to all connected clients
    broadcast(bytes(chatJoinMsg, "utf8"))

    # Keeping track of the connected client names
    clients[client] = clientName

    while True:

        message = client.recv(BUFSIZ)

        if message != bytes("#exit#", "utf8"):
            broadcast(message, clientName + ": ")

        else:
            client.send(bytes("#exit#", "utf8"))
            client.close()
            # Remove client from the list of connected clients
            del clients[client]
            # Display to connected users that client has left the chat
            broadcast(bytes("%s has disconnected." %clientName, "utf8"))
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
