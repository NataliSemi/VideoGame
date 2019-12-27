import pygame
import math
import random

from pygame import mixer

#Initialize the pygame
pygame.init()

#create a screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('player.png')
playerx =370
playery = 480
playerx_change =0

# Enemy
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(4)
    enemyy_change.append(40)


#Bullet
#Ready - you can't see the bullet on the screen
#Fire - your bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 400
bulletx_change = 0
bullety_change = 10
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textx = 10
texty = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx-bulletx, 2)) + (math.pow(enemyy - bullety, 2))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    # RGB red, green, blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get the current x cordinate of the spaceship
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # Check for boundries of spaceship so it doesn't go out
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

        # Enemy Movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyy[i] > 440:
            for j in range(num_of_enemies):
                enemyy[j] = 2000
            game_over_text()
            break


        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 4
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -4
            enemyy[i] += enemyy_change[i]

            # Collision
            collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
            if collision:
                explosion_Sound =mixer.Sound('explosion.wav')
                explosion_Sound.play()
                bullety = 480
                bullet_state = "ready"
                score_value += 1
                enemyx[i] = random.randint(0, 735)
                enemyy[i] = random.randint(50, 150)

            enemy(enemyx[i], enemyy[i], i)

    # Bullet Movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(playerx,bullety)
        bullety -= bullety_change


    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()
