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
basket_y = SCREEN_HEIGHT - BASKET_HEIGHT - 80
score = 0
game_over = False

topping_x = random.randint(0, SCREEN_WIDTH - 30)
topping_y = 0
topping_speed = 3

current_topping = "normal" 

lives = 3

def GameThread():
    global basket_x, basket_y, topping_x, topping_y, topping_speed, basket_speed, score, game_over, current_topping, lives

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Catch the Toppings!")
    font = pygame.font.Font(None, 36)

    # load background image
    image = pygame.transform.scale(pygame.image.load("background.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
    # loading the toppings and scaling them 
    topping_images = [
        pygame.transform.scale(pygame.image.load("anchovy.png").convert_alpha(), (40, 40)),
        pygame.transform.scale(pygame.image.load("pepperoni.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("pepper.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("mushroom.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("olive.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("onion.png").convert_alpha(), (30, 30)),
        pygame.transform.scale(pygame.image.load("sausage.png").convert_alpha(), (30, 30))
    ]

    topping_image = random.choice(topping_images)

    evil_topping_images = [
        pygame.transform.scale(pygame.image.load("applecore.png").convert_alpha(), (40, 40)),
        pygame.transform.scale(pygame.image.load("fishbones.png").convert_alpha(), (40, 40)),
        pygame.transform.scale(pygame.image.load("bananapeel.png").convert_alpha(), (40, 40))
    ]
    evil_topping_image = random.choice(evil_topping_images)
    
    slow_topping_images = [
        pygame.transform.scale(pygame.image.load("poisonbottle.png").convert_alpha(), (40, 40)),
        pygame.transform.scale(pygame.image.load("orangejuice.png").convert_alpha(), (40, 40))
    ]
    slow_topping_image = random.choice(slow_topping_images)

    

    topping_probability = [
        "normal", "normal", "normal", "normal", "evil", "slow", "slow"
    ]

    clock = pygame.time.Clock()

    current_music = "papas.mp3"

    def update_music(score):
        nonlocal current_music
        if score < 5 and current_music != "lowScore.ogg":
            mixer.music.load("lowScore.ogg")
            mixer.music.play(-1)
            current_music = "lowScore.ogg"
        elif 5 <= score < 10 and current_music != "midScore.ogg":
            mixer.music.load("midScore.ogg")
            mixer.music.play(-1)
            current_music = "midScore.ogg"
        elif 10 <= score < 20 and current_music != "highScore.ogg":
            mixer.music.load("highScore.ogg")
            mixer.music.play(-1)
            current_music = "highScore.ogg"
        elif score >= 20 and current_music != "ultHighScore.mpg":
            mixer.music.load("ultHighScore.mpg")
            mixer.music.play(-1)
            current_music = "ultHighScore.mpg"


    show_start_screen = True

    while show_start_screen : 
        start_screen_image = pygame.image.load("royNerv2.png").convert_alpha()
        screen.blit(start_screen_image, (0,0))

        title = font.render("Roy's Pizza Panic!", True, (0,0,0))
        subtext = font.render("Press SPACE to start helping Roy!", True, (0,0,0))
        description = font.render("Help him catch all the pizza toppings", True, (0,0,0))
        description_1 = font.render("and avoid rotten ones!", True, (0,0,0))


        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2 + 75, 100))
        screen.blit(subtext, (SCREEN_WIDTH // 2 - subtext.get_width() // 2 + 75, 160))
        screen.blit(description, (SCREEN_WIDTH // 2 - description.get_width() // 2 + 75, 200))
        screen.blit(description_1, (SCREEN_WIDTH // 2 - description_1.get_width() // 2 + 75, 240))


        basket_sprite = pygame.transform.scale(pygame.image.load("ROYPIZZA.png").convert_alpha(), (100, 150))

        pygame.display.flip()

        for event in pygame.event.get() : 
            if event.type == pygame.QUIT : 
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE : 
                show_start_screen = False 

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
                    basket_y = SCREEN_HEIGHT - BASKET_HEIGHT - 80
                    score = 0
                    topping_speed = 3
                    basket_speed = 20
                    topping_x = random.randint(0, SCREEN_WIDTH - 30)
                    topping_y = 0
                    topping_image = random.choice(topping_images)
                    game_over = False
                    current_topping = "normal"
                    lives = 3 
                    

        update_music(score)
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

            if basket_x < 0 : 
                basket_x = 0
            if basket_x > SCREEN_WIDTH - BASKET_WIDTH : 
                basket_x = SCREEN_WIDTH - BASKET_WIDTH
            
            topping_y += topping_speed

            # collosion detection 
            basket_rect = pygame.Rect(basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT)

            if current_topping == "normal":
                topping_rect = pygame.Rect(topping_x, topping_y, 30, 30)
                if basket_rect.colliderect(topping_rect):
                    score += 1
                    topping_speed += 0.5
                    basket_speed += 3.5
                    topping_x = random.randint(0, SCREEN_WIDTH - 30)
                    topping_y = 0
                    topping_image = random.choice(topping_images)
                    next_topping = random.choice(topping_probability)
                    current_topping = next_topping 
                elif topping_y > SCREEN_HEIGHT:
                    lives -= 1
                    if lives <= 0 : 
                        game_over = True
                    else : 
                        topping_x = random.randint(0, SCREEN_WIDTH - 30)
                        topping_y = 0
                        topping_image = random.choice(topping_images)
                        next_topping = random.choice(topping_probability)
                        current_topping = next_topping
            elif current_topping == "evil": 
                evil_topping_rect = pygame.Rect(topping_x, topping_y, 30, 30)
                if basket_rect.colliderect(evil_topping_rect):
                    game_over = True
                elif topping_y > SCREEN_HEIGHT:
                    topping_x = random.randint(0, SCREEN_WIDTH - 30)
                    topping_y = 0
                    evil_topping_image = random.choice(evil_topping_images)
                    next_topping = random.choice(topping_probability)
                    current_topping = next_topping  
            elif current_topping == "slow":
                slow_topping_rect = pygame.Rect(topping_x, topping_y, 30, 30)
                if basket_rect.colliderect(slow_topping_rect):
                    basket_speed -= 2
                    topping_x = random.randint(0, SCREEN_WIDTH - 30)
                    topping_y = 0
                    slow_topping_image = random.choice(slow_topping_images)
                    next_topping = random.choice(topping_probability)
                    current_topping = next_topping 
                elif topping_y > SCREEN_HEIGHT:
                    topping_x = random.randint(0, SCREEN_WIDTH - 30)
                    topping_y = 0
                    slow_topping_image = random.choice(slow_topping_images)
                    next_topping = random.choice(topping_probability)
                    current_topping = next_topping  


            

        # Draw everything
        if current_topping == "normal":
            screen.blit(topping_image, (topping_x, topping_y))
        elif current_topping == "evil":
            screen.blit(evil_topping_image, (topping_x, topping_y))
        elif current_topping == "slow":
            screen.blit(slow_topping_image, (topping_x, topping_y))

        screen.blit(basket_sprite, (basket_x, basket_y))

        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        lives_text = font.render("Lives: " + str(lives), True, (0, 0, 0))
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))


        if game_over:
            mixer.music.stop()
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
        # elif data == 'w' : 
        #     basket_y -= basket_speed
        # elif data == 's' : 
        #     basket_y += basket_speed

        if basket_x < 0 : 
            basket_x = 0
        if basket_x > SCREEN_WIDTH - BASKET_WIDTH : 
            basket_x = SCREEN_WIDTH - BASKET_WIDTH
            

        if data == 'r' : 
            game_over = False
            topping_speed = 3 
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