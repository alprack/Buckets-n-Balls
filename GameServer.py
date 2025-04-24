import pynput 
from pynput import keyboard
import random
import socket
import time
import pygame
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

def GameThread():
    global basket_x, basket_y, topping_x, topping_y, topping_speed, basket_speed, score, game_over

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

    clock = pygame.time.Clock()

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
                    basket_speed = 20
                    topping_x = random.randint(0, SCREEN_WIDTH - 30)
                    topping_y = 0
                    topping_image = random.choice(topping_images)
                    game_over = False

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

            topping_y += topping_speed

            # collosion detection 
            basket_rect = pygame.Rect(basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT)
            topping_rect = pygame.Rect(topping_x, topping_y, 30, 30)

            # checking for collision between the basket and topping
            # basically, if the player missed a topping 
            if basket_rect.colliderect(topping_rect):
                score += 1
                topping_speed += 0.5
                basket_speed += 3.5
                topping_x = random.randint(0, SCREEN_WIDTH - 30)
                topping_y = 0
                topping_image = random.choice(topping_images)

            # if the topping has fallen past the screen, GAME OVER 
            if topping_y > SCREEN_HEIGHT:
                game_over = True

        # Draw everything
        screen.blit(topping_image, (topping_x, topping_y))
        pygame.draw.rect(screen, (0, 0, 200), (basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT))

        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        if game_over:
            over_text = font.render("GAME OVER! Press R to Restart!", True, (255, 0, 0))
            screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

def ServerThread() : 
    global basket_x, basket_y, game_over, topping_speed, basket_speed, topping_y, score

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
        elif data == 'w' : 
            basket_y -= basket_speed
        elif data == 's' : 
            basket_y += basket_speed
        if data == 'r' : 
            game_over = False
            topping_speed = 3
            basket_speed = 20 
            topping_y = 0 
            score = 0 
            print("Game restarted")
        
    conn.close() 

def main():
    t2 = threading.Thread(target=ServerThread, args=[])
    t2.start()  

    GameThread()  

    t2.join() 

if __name__ == "__main__":
    main()
