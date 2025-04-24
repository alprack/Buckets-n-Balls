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
            time.sleep(0.1)
        elif key.char == 'd' : 
            client_socket.send('d'. encode())
            time.sleep(0.1)
        elif key.char == 's' : 
            client_socket.send('s'.encode())
            time.sleep(0.1)
        elif key.char  == 'w' : 
            client_socket.send('w'.encode())
            time.sleep(0.1)
        elif key.char == 'r' : 
            client_socket.send('r'.encode())
    except AttributeError :
        pass 


def client_program():
    print("trying to connect to server")
    host = "10.14.92.36"
    port = 5003  # socket server port number

    global client_socket
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print("waiting for keyboard input")
    listener = keyboard.Listener(on_press=on_press)
    listener.start() 

    try : 
        while True : 
            time.sleep(0.1)
    except KeyboardInterrupt : 
        pass 
    finally : 
        client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()