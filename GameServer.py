import pynput 
from pynput import keyboard
import random
import socket
import time
import pygame
from pygame import mixer
import sys
import threading 

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Basket settings
BASKET_WIDTH = 100
BASKET_HEIGHT = 20

# Game state variables
basket_speed = 20
basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
basket_y = SCREEN_HEIGHT - BASKET_HEIGHT - 10
score = 0
game_over = False

topping_x = random.randint(0, SCREEN_WIDTH - 30)
topping_y = 0
topping_speed = 3

evil_topping_x = random.randint(0, SCREEN_WIDTH - 30)
evil_topping_y = 0
evil_topping_speed = 3

slow_topping_x = random.randint(0, SCREEN_WIDTH - 30)
slow_topping_y = 0
slow_topping_speed = 3

current_topping = "normal" 


def GameThread():
    global basket_x, basket_y, topping_x, topping_y, topping_speed, basket_speed, score, game_over, evil_topping_x, evil_topping_y, evil_topping_speed, slow_topping_x, slow_topping_y, slow_topping_speed, current_topping

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Catch the Toppings!")
    font = pygame.font.Font(None, 36)

    # load background image
    image = pygame.transform.scale(pygame.image.load("background.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
    # loading the toppings and scaling them 
    topping_images = [
        pygame.transform.scale(pygame.image.load("anchovy.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("pepperoni.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("pepper.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("mushroom.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("olive.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("onion.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("sausage.png").convert_alpha(), (30, 30))
    ]

    topping_image = random.choice(topping_images)

    evil_topping_images = [
        pygame.transform.scale(pygame.image.load("applecore.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("fishbones.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("bananapeel.png").convert_alpha(), (30, 30))
    ]
    evil_topping_image = random.choice(evil_topping_images)
    
    slow_topping_images = [
        pygame.transform.scale(pygame.image.load("poisonbottle.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("orangejuice.png").convert_alpha(), (30, 30))
    ]
    slow_topping_image = random.choice(slow_topping_images)

    basket_sprite = pygame.transform.scale(pygame.image.load("ROYPIZZA.png").convert_alpha(), (85, 45))
    

    topping_probability = [
        "normal", "slow"
    ]

    clock = pygame.time.Clock()

    mixer.init()

    mixer.music.load("papas.mp3")
    mixer.music.play(-1) 
    mixer.music.set_volume(0.7) 

    while True:
        screen.blit(image, (0, 0))
        #screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    # reset game after player loses 
                    basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
                    basket_y = SCREEN_HEIGHT - BASKET_HEIGHT - 10
                    score = 0
                    topping_speed = 3
                    evil_topping_speed = 3
                    slow_topping_speed = 3
                    basket_speed = 20
                    topping_x = random.randint(0, SCREEN_WIDTH - 30)
                    topping_y = 0
                    topping_image = random.choice(topping_images)
                    game_over = False
                    current_topping = "normal"

        keys = pygame.key.get_pressed()
        if not game_over:
        # just moving based on user input 
            if keys[pygame.K_a]:
                basket_x -= basket_speed
            if keys[pygame.K_d]:
                basket_x += basket_speed
           #if keys[pygame.K_w] : 
           #     basket_y -= basket_speed
           # if keys[pygame.K_s] : 
           #     basket_y += basket_speed

            if current_topping == "normal":
                topping_y += topping_speed
            elif current_topping == "evil":
                evil_topping_y += evil_topping_speed
            elif current_topping == "slow":
                slow_topping_y += slow_topping_speed

            # collosion detection 
            basket_rect = pygame.Rect(basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT)

            if current_topping == "normal":
                topping_rect = pygame.Rect(topping_x, topping_y, 30, 30)
                if basket_rect.colliderect(topping_rect):
                    score += 1
                    topping_speed += 0.5
                    evil_topping_speed += 0.5
                    slow_topping_speed += 0.5
                    basket_speed += 3.5
                    topping_x = random.randint(0, SCREEN_WIDTH - 30)
                    topping_y = 0
                    topping_image = random.choice(topping_images)
                    next_topping = random.choice(topping_probability)
                    current_topping = next_topping 
                elif topping_y > SCREEN_HEIGHT:
                    game_over = True   
            elif current_topping == "evil":  # Evil topping logic
                evil_topping_rect = pygame.Rect(evil_topping_x, evil_topping_y, 30, 30)
                if basket_rect.colliderect(evil_topping_rect):
                    game_over = True
                elif evil_topping_y > SCREEN_HEIGHT:
                    evil_topping_x = random.randint(0, SCREEN_WIDTH - 30)
                    evil_topping_y = 0
                    evil_topping_image = random.choice(evil_topping_images)
                    next_topping = random.choice(topping_probability)
                    current_topping = next_topping  
            elif current_topping == "slow":
                slow_topping_rect = pygame.Rect(slow_topping_x, slow_topping_y, 30, 30)
                if basket_rect.colliderect(slow_topping_rect):
                    basket_speed -= 1
                    slow_topping_x = random.randint(0, SCREEN_WIDTH - 30)
                    slow_topping_y = 0
                    slow_topping_image = random.choice(slow_topping_images)
                    next_topping = random.choice(topping_probability)
                    current_topping = next_topping 
                elif slow_topping_y > SCREEN_HEIGHT:
                    slow_topping_x = random.randint(0, SCREEN_WIDTH - 30)
                    slow_topping_y = 0
                    slow_topping_image = random.choice(slow_topping_images)
                    next_topping = random.choice(topping_probability)
                    current_topping = next_topping  


            

        # Draw everything
        if current_topping == "normal":
            screen.blit(topping_image, (topping_x, topping_y))
        elif current_topping == "evil":
            screen.blit(evil_topping_image, (evil_topping_x, evil_topping_y))
        elif current_topping == "slow":
            screen.blit(slow_topping_image, (slow_topping_x, slow_topping_y))

        screen.blit(basket_sprite, (basket_x, basket_y))

        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        if game_over:
            over_text = font.render("GAME OVER! Press R to Restart!", True, (255, 0, 0))
            screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

def ServerThread() : 
    global basket_x, basket_y, game_over, topping_speed, basket_speed, topping_y, score, evil_topping_speed, evil_topping_y

    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  
    host = s.getsockname()[0]  
    s.close()
    print(f"Server IP: {host}")
    port = 5003  

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    print("Server enabled...")
    server_socket.listen(2)

    conn, address = server_socket.accept()  
    client_ip = address[0] 
    print(f"Connection from client IP: {client_ip}")

    while True : 
        data = conn.recv(1024).decode()
        if not data : 
            break 

        if data == 'a' :
            basket_x -= basket_speed
        elif data == 'd' : 
            basket_x += basket_speed
        # elif data == 'w' : 
        #     basket_y -= basket_speed
        # elif data == 's' : 
        #     basket_y += basket_speed

        if data == 'r' : 
            game_over = False
            topping_speed = 3
            evil_topping_speed = 3 
            basket_speed = 20 
            topping_y = 0 
            score = 0 

    conn.close() 

def main():
    t2 = threading.Thread(target=ServerThread, args=[])
    t2.start()  

    GameThread()  
    t2.join() 

if __name__ == "__main__":
    main()