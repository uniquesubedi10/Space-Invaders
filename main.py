import pygame
import random
import math
from pygame import mixer
#Initialize the pygame
pygame.init()

#Create the screen
screen=pygame.display.set_mode((800,600),pygame.RESIZABLE)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("icon.png")
pygame.display.set_icon(icon)

#background
background=pygame.image.load("background.png")
#Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)
#Score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10
def show_score(x,y):
   score=font.render("Score: "+str(score_value),True,(255,255,255))
   screen.blit(score,(x,y))

#Player
playerImg=pygame.image.load("spaceshooter.png")
playerX=370
playerY=480
playerX_change=0
playerY_change=0

def player(x,y):
    screen.blit(playerImg,(x,y))

enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6
i=6
for i in range(num_of_enemies):
   enemyImg.append(pygame.image.load("enemy.png"))
   enemyX.append(random.randint(0,735))
   enemyY.append(random.randint(64,300))
   enemyX_change.append(1)
   enemyY_change.append(40)

def enemy1(x,y,i):
   screen.blit(enemyImg[i],(x,y))

#Bullet
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletY_change=5
#Ready state -You can't see the bullet
bullet_state="ready"
#Fire state- Bullet is moving 
def bulletFire(x,y):
   global bullet_state
   bullet_state="Fire"
   screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
   distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
   if distance<27:
      return True
   else:
      return False

#Game Over
over_font=pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
   over_text=over_font.render("GAME OVER",True,(255,255,255))
   screen.blit(over_text,(200,250))



color=(100,0,0)
#Game Loop
running=True
while running:
    screen.fill((0,0,0))
    #Background Image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        #If keystroke is pressed check whether its right or left
        if event.type==pygame.KEYDOWN:#Keydown for event of pressing key
            if event.key==pygame.K_LEFT or event.key==pygame.K_a:
             playerX_change= -5
            if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
             playerX_change=5
            if event.key==pygame.K_SPACE:
              if bullet_state is "ready":
               bullet_sound=mixer.Sound("laser.wav")
               bullet_sound.play()
               #Get the current X-coordinate of the player spaceship 
               bulletX=playerX
               bulletFire(bulletX,bulletY)

        if event.type==pygame.KEYUP:#Keyup for released event
            if (event.key==pygame.K_RIGHT or event.key==pygame.K_d)or(event.key==pygame.K_LEFT or event.key==pygame.K_a):
              playerX_change=0
            if (event.key==pygame.K_DOWN or event.key==pygame.K_s) or(event.key==pygame.K_UP or event.key==pygame.K_w):
              playerY_change=0
         

    #Checking boundaries of spaceship so it doesnt go out of bound
    playerX +=playerX_change
    playerY +=playerY_change
    if playerX<=0:
       playerX=0
    elif playerX>=736:
       playerX=736
    if playerY<=0:
       playerY=0
    elif playerY>=536:
       playerY=536
   
   #Enemy Movement
    for i in range(num_of_enemies):
      #Game Over 
      if enemyY[i]>430:
         for j in range(num_of_enemies):
            enemyY[j]=2000
         game_over_text()
         break
      enemyX[i]+=enemyX_change[i]
      if enemyX[i]<=0:
         enemyX_change[i]=1
         enemyY[i]+=enemyY_change[i]
      elif enemyX[i]>=736:
         enemyX_change[i]=-1
         enemyY[i]+=enemyY_change[i]
       #Collision
      collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
      if collision:
         explosion_sound=mixer.Sound("explosion.wav")
         explosion_sound.play()
         bulletY=480
         bullet_state="ready"
         score_value+=1
         enemyX[i]=random.randint(0,735)
         enemyY[i]=random.randint(64,300)
      enemy1(enemyX[i],enemyY[i],i)

   #Bullet Movement
    if bulletY<=0:
       bulletY=480 
       bullet_state="ready"
    
    if bullet_state is "Fire":
       bulletFire(bulletX,bulletY)
       bulletY-=bulletY_change

    
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
    
pygame.quit()