import pygame, sys
import random
import math
from pygame import mixer
# set up pygame
pygame.init()

# create the screen
screenX = 800
screenY = 600
screen = pygame.display.set_mode((screenX,screenY))

# Background
backgroundImg = pygame.image.load('background.jpg')


# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 520
playerChangeX = 0

# Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = []
enemyY = []
enemy_speed = []
enemy_speed_down = 40
num_of_enemies = 10
explosion_sound = mixer.Sound('explosion.wav')

for i in range(num_of_enemies):
    enemyX.append(random.randint(0,screenX-64))
    enemyY.append(200)
    enemy_speed.append(0.4)


bulletImg = pygame.image.load('bullet.png')

bulletX = random.randint(0,screenX-64)
bulletY = 480
bullet_speed_Y = 40
bullet_state = "ready"
bullet_sound = mixer.Sound('laser.wav')
# read -> bullet is ready to be fired
# fired -> bullet is travelling

def player(x, y):
    screen.blit(playerImg, (int(x), int(y)))

def enemy(x, y):
    screen.blit(enemyImg, (int(x), int(y)))

def fire_bullet(x,y):
    screen.blit(bulletImg, (x+16, y+10))

def hasCollided(x1,y1,x2,y2):
    distance = math.sqrt(math.pow(x1 - x2,2) + math.pow(y1 - y2,2))
    if distance < 27:
        return True
    return False

# Game Loop
running = True
firing = False

#score
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
fontOver = pygame.font.Font('freesansbold.ttf',64)

def show_score(score):
    score_text = font.render("Score: {}".format(score),True, (255,255,255))
    screen.blit(score_text,(10,10))

def game_over_text():
    score_text = fontOver.render("Game Over",True, (255,255,255))
    screen.blit(score_text,(200,250))

while running:
    screen.fill((0,0,0))
    screen.blit(backgroundImg,(0,0))
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == 97:
                playerChangeX+=0.7
            if event.key == pygame.K_RIGHT or event.key == 100:
                playerChangeX-=0.7
            if event.key == 32:
                firing = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == 97:
                playerChangeX-=0.7
            if event.key == pygame.K_RIGHT or event.key == 100:
                playerChangeX+=0.7
            if event.key == 32:
                firing = True

    for i in range(num_of_enemies):
        enemyX[i] += enemy_speed[i]
        if enemyX[i] <= 0:
            enemy_speed[i] = 0.4
            enemyY[i] += enemy_speed_down
        if enemyX[i] > screenX - 64:
            enemy_speed[i] = -0.4
            enemyY[i] += enemy_speed_down


    playerX+=playerChangeX
    if playerX <= 0:
        playerX = 0
    if playerX > screenX - 64:
        playerX = screenX - 64

    if firing == True and bullet_state == "ready":
        bullet_sound.play()
        bulletY = playerY
        bulletX = playerX
        bullet_state = "fired"

    if bullet_state == "fired":
        fire_bullet(bulletX,bulletY)
        bulletY -= 4

    if bulletY < 0:
        bullet_state = "ready"


    #Collision
    for i in range(num_of_enemies):
        if hasCollided(enemyX[i],enemyY[i],bulletX,bulletY):
            bullet_state = "ready"
            explosion_sound.play()
            bulletY = playerY
            score+=1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)

        if enemyY[i] > 200:
            for i in range(num_of_enemies):
                enemyY[i] = 2000

            game_over_text()
            break

    player(playerX,playerY)
        enemy(enemyX[i],enemyY[i])

    show_score(score)

    pygame.display.update()

