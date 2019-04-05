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

# Import Tkinter for GUI
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


def send(event=None):

    message = myMessage.get()

    # Makes input field blank when 'send' button is pressed
    myMessage.set("")

    clientSocket.send(bytes(message, "utf8"))

    if message == "#exit#":
        clientSocket.close()

        # Quitting the UI window on exit, 'window' is the tkinter window variable
        window.quit()


# Method to handle the user closing the window without exiting the chat first
def quit(event=None):

    myMessage.set("#exit#")

    send()


# GUI Creation and Customization

# Creating the base GUI
window = tkinter.Tk()

# Title of window
window.title("TextTalker")

messageFrame = tkinter.Frame(window, width=100)

myMessage = tkinter.StringVar()

myMessage.set("Enter message here.")

scrollbar = tkinter.Scrollbar(messageFrame)

# Handling how messages are displayed
messageList = tkinter.Listbox(messageFrame, height=15, width=100, yscrollcommand=scrollbar.set)

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

messageList.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)

messageList.pack()

messageFrame.pack()

inputField = tkinter.Entry(window, textvariable=myMessage, width=75)

inputField.bind("<Return>", send)

inputField.pack()

buttonSend = tkinter.Button(window, text="Send", command=send)

buttonSend.pack()

window.protocol("WM_DELETE_WINDOW", quit)


# Client --> Server Connection
HOST = input("Enter host IP: ")

PORT = int(input("Enter host Port:"))

SERVERADDR = (HOST, PORT)

BUFSIZ = 1024

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect(SERVERADDR)

receiveThread = Thread(target=receive)

receiveThread.start()

tkinter.mainloop()
