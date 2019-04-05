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

#Import Tkinter for GUI
import tkinter


# For recieving messages from the server
def receive():

    while True:

        try:
            message = clientSocket.recv(BUFSIZ).decode("utf8")
            messageList.insert(tkinter.END, message)

        except OSError:
            # Error handling for client leaving
            break


def send(event = None):

    message = myMessage.get()

    myMessage.set("")

    clientSocket,send(bytes(message, "utf8"))

    if message == "#exit#":
        clientSocket.close()

        # Quitting the UI window on exit, 'window' is the tkinter window variable
        window.quit()


# Method to handle the user closing the window without exiting the chat first
def closing(event = None):

    myMessage.set("#exit#")

    send()

