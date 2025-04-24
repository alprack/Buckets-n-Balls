import pynput 
from pynput import keyboard
import random
import socket
import time
import pygame

pygame.init()

def on_press(key) : 
    try : 
        if key.char == 'a' : 
            client_socket.send('a'.encode())
        elif key.char == 'd' : 
            client_socket.send('d'. encode())
        elif key.char == 's' : 
            client_socket.send('s'.encode())
        elif key.char  == 'w' : 
            client_socket.send('w'.encode())
        elif key.char == 'r' : 
            client_socket.send('r'.encode())
    except AttributeError :
        pass 


def client_program():
    print("trying to connect to server")
    host = "10.14.92.93"
    port = 5003  # socket server port number

    global client_socket
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print("waiting for keyboard input")
    listener = keyboard.Listener(on_press=on_press)
    listener.start() 

    try : 
        while True : 
            pass
    except KeyboardInterrupt : 
        pass 
    finally : 
        client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()