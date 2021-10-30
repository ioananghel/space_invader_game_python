#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 11:41:32 2020

@author: ioan
"""

import pygame
from sys import exit
import random
import math
from pygame import mixer

#initialize the pygame
pygame.init()

#background
background = pygame.image.load("background_final_version.png")

#backgorund sound
mixer.music.load("background.wav")
mixer.music.play( -1 )

#create the screem
screen = pygame.display.set_mode( (800, 600) )

#Title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append( pygame.image.load("enemy.png") )
    enemyX.append( random.randint(0, 735) )
    enemyY.append( random.randint(0, 150) )
    enemyX_change.append( 1 )
    enemyY_change.append( 40 )

#Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready" #<=> you can't see the bullet on the screen
#"fire" <=> the bullet is currently moving

#Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit( score, (x, y) )

def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit( over_text, (200, 250) )

def player(x, y):
    screen.blit(playerImg, (x, y) )
    
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y) )

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10) )

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt( (math.pow(enemyX - bulletX , 2)) + (math.pow(enemyY - bulletY, 2)) )
    if distance < 27:
        return True
    return False


#Game loop
running = True
while running:
    screen.fill( (0, 0, 0) ) #RGB
    screen.blit(background, (0, 0) )
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            #running = False                
        #if keystroke is pressed we check wether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
                #print("Left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
                #print("Right arrow is pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":#Get the current coordinate of the bullet
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                #print("Keystroke has been released")
    
    #Creating boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    for i in range(num_enemies):
        
        #Game Over
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[i] = 2000
            game_over_text()
            break
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 150)
        enemy(enemyX[i], enemyY[i], i) #Drawing the enemy image
        
    #Bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change   
    
    player(playerX, playerY) #Drawing the player image
    show_score(textX, textY)
    pygame.display.update()