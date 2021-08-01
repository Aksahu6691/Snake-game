author = "Akash Sahu"

import pygame
import random
import os

# Initialization
pygame.mixer.init()
pygame.init()

# Colours
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
snakegreen = (35, 45, 40)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Backgrounds
img = pygame.image.load("Image/bg2.jpg")
img = pygame.transform.scale(img, (screen_width, screen_height)).convert_alpha()
intro = pygame.image.load("Image/bg.jpg")
outro = pygame.image.load("Image/outro.png")

# Game Title
pygame.display.set_caption("SnakesWithAkash")
pygame.display.update()

# Outer Music
pygame.mixer.music.load('Music/wc.mp3')
pygame.mixer.music.play(100)
#pygame.mixer.music.set_volume(.6)

# Variables For The Game
clock = pygame.time.Clock()
font = pygame.font.SysFont('Rosewood Std Regular', 45)

def text_screen(text, colour, x, y):
    screen_text = font.render(text, True, colour)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, colour, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, colour, [x, y, snake_size, snake_size])

# Welcome Window
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(intro, (0,0))
        #gameWindow.fill((255,0,127))
        text_screen("Welcome to Snakes", black, 240, 220)
        text_screen("Press Enter To Play", black, 230, 260)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    # inner Music
                    #pygame.mixer.music.fadeout(200)
                    pygame.mixer.music.load('Music/inner.mp3')
                    pygame.mixer.music.play()
                    #pygame.mixer.music.set_volume(.6)
                    gameloop()

        pygame.display.update()
        clock.tick(60)

# Game Loop
def gameloop():

    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    # Check if high score file exists
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    # Food
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)

    # Game variable
    score = 0
    #init_velocity = 2
    init_velocity = 5
    #init_velocity = 7
    #init_velocity = 9
    snake_size = 20
    fps = 60
    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            # Game over screen
            #gameWindow.fill(white)
            gameWindow.blit(outro, (0, 0))
            #text_screen("Game Over! Press Enter To Continue", red, 100, 250)
            text_screen("Score: " + str(score), snakegreen, 350, 370)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    # Cheat code
                    if event.key == pygame.K_q:
                        score +=10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<10 and abs(snake_y - food_y)<10:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5
                if score>int(hiscore):
                    hiscore = score

            gameWindow.blit(img, (0, 0))
            text_screen("Score: " + str(score) + "  Hiscore: "+str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('Music/end.mp3')
                pygame.mixer.music.play()
                #pygame.mixer.music.set_volume(.6)

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('Music/end1.mp3')
                pygame.mixer.music.play()
                #pygame.mixer.music.set_volume(.6)

            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()