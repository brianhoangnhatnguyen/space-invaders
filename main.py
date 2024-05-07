import math
import pygame
import random
from pygame import mixer

# initialize pygame
pygame.init()

# create game screen
screen = pygame.display.set_mode((800, 720))
running_screen = True

# set title and icon
pygame.display.set_caption("space invaders")
pygame.display.set_icon(pygame.image.load("icon.png"))

# main part
player = pygame.image.load("space_ship (2) (1).png")
playerX_change = 0
playerX = 380
playerY = 550
background = pygame.image.load("bg image.png")

# music
mixer.music.load('background.wav')
mixer.music.play(-1)

# score part
score_value = 0

# font part
font = pygame.font.Font('EtArtiluxRegular-ARRvD.ttf', 60)
textX = 300
textY = 10

# game over text
gameover_font = pygame.font.Font('EtArtiluxRegular-ARRvD.ttf', 100)

# alien part
alien = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
nums_aliens = 6

for i in range(nums_aliens):
    alien.append(pygame.image.load("alien.png"))
    alienX.append(random.randint(0, 800))
    alienY.append(random.randint(50, 200))
    alienX_change.append(0.5)
    alienY_change.append(40)

# laser part
laser_beam = pygame.image.load("laser beam (2).png")
laser_beamX = 0
laser_beamY = 500
laserY_change = 0.5
laser_state = 'Ready'  # ready means the laser is hidden
laser_state2 = 'Fire'  # fire means the laser will move upwards


def player_image():
    screen.blit(player, (playerX, playerY))


def alien_image(X, Y, i):
    screen.blit(alien[i], (X,Y))


def collision(alienX, alienY, laser_beamX, laser_beamY):
    distance = math.sqrt(math.pow(alienX - laser_beamX, 2) + math.pow(alienY - laser_beamY, 2))
    if distance < 50:
        return True
    else:
        return False


def fire_laser(x, y):
    global laser_state
    laser_state = 'Fire'
    screen.blit(laser_beam, (x + 16, y + 10))


def show_score(X, Y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (X, Y))


def gameover_screen():
    gameover_text = gameover_font.render('Game Over!', True, (255, 255, 255))
    screen.blit(gameover_text, (175, 300))

# game loop
while running_screen:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_screen = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -0.5

            if event.key == pygame.K_d:
                playerX_change = 0.5

            if event.key == pygame.K_SPACE:
                laser_beamX = playerX
                fire_laser(laser_beamX, laser_beamY)
                laser_sound = mixer.Sound('laser.wav')
                laser_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    playerX += playerX_change

    # player boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # alien movement
    for i in range(nums_aliens):
        # game over
        if alienY[i] > 400:
            for j in range(nums_aliens):
                alienY[j] = 1500
            gameover_screen()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 0.5
            alienY[i] += alienY_change[i]

        elif alienX[i] >= 736:
            alienX_change[i] = -0.5
            alienY[i] += alienY_change[i]

        is_collision = collision(alienX[i], alienY[i], laser_beamX, laser_beamY)
        if is_collision:
            laser_beamY = 500
            laser_state = 'Ready'
            score_value += 1
            alienX[i] = random.randint(0, 700)
            alienY[i] = random.randint(50, 200)
            explosion = mixer.Sound('explosion.wav')
            explosion.play()

        alien_image(alienX[i], alienY[i], i)

    # laser
    if laser_beamY <= 0:
        laser_beamY = 500
        laser_state = 'Ready'

    if laser_state is 'Fire':
        fire_laser(laser_beamX, laser_beamY)
        laser_beamY -= laserY_change

    player_image()
    show_score(textX, textY)
    pygame.display.update()
