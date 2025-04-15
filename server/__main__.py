import pynput 
from pynput import keyboard
import random
import socket
import time
import pygame
import sys

# Initialize pygame
pygame.init()

# Ball seting
BALL_RADIUS = 15
BALL_FALL_SPEED = 5

# Basket setting
BASKET_WIDTH = 100
BASKET_HEIGHT = 20

#Game variables
basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
basket_y = SCREEN_HEIGHT - BASKET_HEIGHT -10
ball_x = random.randint(0, SCREEN_WIDTH-BALL_RADIUS)
ball_y = 0
score = 0