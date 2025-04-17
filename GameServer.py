import pynput 
from pynput import keyboard
import random
import socket
import time
import pygame
import sys

# screen dimension
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Initialize pygame
pygame.init()

# Ball seting
BALL_RADIUS = 15


# Basket setting
BASKET_WIDTH = 100
BASKET_HEIGHT = 20

#Game variables
basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
basket_y = SCREEN_HEIGHT - BASKET_HEIGHT -10
ball_x = random.randint(0, SCREEN_WIDTH-BALL_RADIUS)
ball_y = 0
score = 0
ball_speed = 3 
basket_speed = 5 
game_over = False 

def GameThread() : 
    global basket_x, basket_x, ball_x, ball_y, basket_speed, basket_speed
    global score, game_over 

    pygame.init() 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Catch the Toppings!")
    
    while True : 
        for event in pygame.event.get() : 
            if event.type == pygame.QUIT : 
                pygame.quit()
                sys.quit() 
            
        if not game_over : 
            ball_y += ball_speed

            # rect is collosion detection 
            basket_rect = pygame.Rect(basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT)
            ball_rect = pygame.Rect(ball_x, ball_y, BALL_RADIUS, BALL_RADIUS)

            collosion = basket_rect.collidedict(ball_rect)

            if collosion : 
                score += 1
                ball_speed += 0.5
                basket_speed += 0.5 
                ball_x = random.randint(0, SCREEN_WIDTH - BALL_RADIUS)
                ball_y = 0

            if ball_y > SCREEN_HEIGHT : 
                game_over = True 
        
        screen.fill

            
            



