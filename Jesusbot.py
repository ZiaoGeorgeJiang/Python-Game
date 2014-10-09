# Jesusbot.py
# by: George Jiang, Ryan Chan, Edward Dong, Alex Jin
# This program is a top down shooter game. Where Jesusbot tries
# to save the humanity and destroys all the evil robots.

#----------------------Import----------------------------
#Import pygame, random, operater
import pygame
from random import randrange, randint
from pygame.locals import *
pygame.mixer.init
pygame.init()
import operator

#Import Images
img = pygame.image.load("background.jpg")
ground = pygame.image.load("ground.jpg")
ground2 = pygame.image.load("ground2.jpg")
story = pygame.image.load("Jesusbot story.png")
robot = pygame.image.load("robot.png")

#Set Screen size
screen = pygame.display.set_mode(img.get_size()) 
pygame.display.set_caption("Jesusbot!")
img = img.convert() 

#Import Text fonts and size
highscoretitlefont = pygame.font.Font("weird_science_nbp.ttf", 70)
highscorefont = pygame.font.Font("Pixel LCD-7.ttf", 50)
my_font = pygame.font.Font("Spac3 halftone.ttf", 58)
my_font2 = pygame.font.Font("Audiowide-Regular.ttf", 48)
my_font2.set_bold(True)
my_font2.set_underline(True)
#---------------------------------------------------

#-------------------------Classes-----------------------------

#Main Character the Jesusbot
class Player(pygame.sprite.Sprite):
    #Initiate sprite
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.down = []
        self.left = []
        self.right = []
        self.up = []
        #Load sprite cuts part of the image and makes it into animation
        self.image = pygame.image.load("annihilatorwn0.png")
        self.image.set_colorkey((24,150,118))
        for a in range(1,5,1):
            self.down.append(self.image.subsurface((64*(a-1),0,64,64)))
        for x in range(1,5,1):
            self.left.append(self.image.subsurface((64*(x-1),64,64,64)))
        for k in range(1,5,1):
            self.right.append(self.image.subsurface((64*(k-1),128,64,64)))
        for j in range(1,5,1):
            self.up.append(self.image.subsurface((64*(j-1),192,64,64)))
        #Attributes
        self.rect = self.down[0].get_rect()
        self.rect[0:2] = pos
        self.lasertimer = 0
        self.lasermax = 10
        self.health = 5
        self.shield = 0
        #Direction
        self.dx = 0
        self.dy = 0

    #Update Movements
    def update(self):
        self.rect.move_ip((self.dx,self.dy))
        newpos = self.rect
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        #Laser sound
        fire = pygame.mixer.Sound("laser.ogg")
        #Edge of the screen
        if newpos[0] < 0:
            self.rect[0] = 0
        elif newpos[0] > screen.get_width() - 64:
            self.rect[0] = screen.get_width() - 64
        if newpos[1] < 0:
            self.rect[1] = 0
        elif newpos[1] > screen.get_height() - 64:
            self.rect[1] = screen.get_height() - 64
        global missile_group
        
        #Movements when key pressed and fire laser
        if keys[K_DOWN]: #if the character is moving down
            self.missilestate = "down"#Direction of the Laser
            if keys[K_SPACE]: #Fire laser
                self.lasertimer += 1 #Laser timer
                if self.lasertimer == self.lasermax:#To prevent from spamming Lasers
                    #Add laser to the sprite group
                    missile_group.add(Missile((self.rect.bottomleft[0]+10,self.rect.bottomleft[1]),self.missilestate))
                    self.lasertimer = 0 #Reset the timers
                    fire.play() #sound of the laser

        #Movements when key pressed and fire laser
        elif keys[K_RIGHT]:#if the character is moving down
            self.missilestate = "right"#Direction of the Laser
            if keys[K_SPACE]:#Fire laser
                self.lasertimer += 1#Laser timer
                if self.lasertimer == self.lasermax:#To prevent from spamming Lasers
                        #Add laser to the sprite group
                        missile_group.add(Missile((self.rect.midright[0],self.rect.midright[1]),self.missilestate))
                        self.lasertimer = 0#Reset the timers
                        fire.play() #sound of the laser
        elif keys[K_UP]:
            self.missilestate = "up"
            if keys[K_SPACE]:
                self.lasertimer += 1
                if self.lasertimer == self.lasermax:
                        missile_group.add(Missile((self.rect.topright[0]-15,self.rect.topright[1]-5),self.missilestate))
                        self.lasertimer = 0
                        fire.play()
        elif keys[K_LEFT]:
            self.missilestate = "left"
            if keys[K_SPACE]:
                self.lasertimer += 1
                if self.lasertimer == self.lasermax:
                        missile_group.add(Missile((self.rect.topleft[0]-10,self.rect.topleft[1]+40),self.missilestate))
                        self.lasertimer = 0
                        fire.play()
        elif keys[K_SPACE]:
            self.lasertimer += 1
            self.missilestate = "down"
            if self.lasertimer == self.lasermax:
                    missile_group.add(Missile((self.rect.bottomleft[0]+10,self.rect.bottomleft[1]),self.missilestate))
                    self.lasertimer = 0
                    fire.play()       
#Enemy Missile class
class eMissile(pygame.sprite.Sprite):
    #Initiate sprite
    def __init__(self,pos,state):
        pygame.sprite.Sprite.__init__(self)
        #Loads sprite Image
        self.image = pygame.image.load("greenLaserRay.png")
        self.image = pygame.transform.scale(self.image, (25,25))
        self.image = pygame.transform.rotate(self.image, 90)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.state = state
        #Direction
        if self.state == "left" or self.state == "right":
            self.image = pygame.transform.rotate(self.image, 90)

    #Unpdate the missile    
    def update(self):
        
        #Deletes missile when it hits the edge of the screen
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > 1000:
            self.kill()

        #Deletes missile when it hits Jesusbot
        elif self.rect.colliderect(jesusbot):
            self.kill()

            #Lowers Jesusbot's health or shield
            if jesusbot.shield > 0:
                jesusbot.shield -= 1
            else:
                jesusbot.health -= 1

        #Shoots in a certain direction
        else:
            if self.state == "left":
                self.rect.move_ip(-20,0)
            elif self.state == "right":
                self.rect.move_ip(20,0)
            else:
                self.rect.move_ip(0,-20) #Up

#Final Boss Class                
class Boss(pygame.sprite.Sprite):

    #Initiates sprite
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        
        #Loads Image
        self.image = pygame.image.load("robot2iceaxe.png")
        self.left = []
        self.right = []
        self.up = []

        #Cuts imgae to parts and loads it into a list for animation
        for x in range(1,5,1):
            self.pic = self.image.subsurface((64*(x-1),80,63.75,50)) #Cuts
            self.pic = pygame.transform.scale(self.pic,(100,100)) #Transforms and scales
            self.left.append(self.pic) #Adds to list
        for j in range(1,5,1):
            self.pic = self.image.subsurface((64*(j-1),144,63.75,50))
            self.pic = pygame.transform.scale(self.pic,(100,100))
            self.right.append(self.pic)
        for k in range(1,5,1):
            self.pic = self.image.subsurface((61*(k-1),204,63.75,50))
            self.pic = pygame.transform.scale(self.pic,(100,100))
            self.up.append(self.pic)

        #Attributes
        self.health = 100

        #Direction and orientation
        self.image = self.up[0]
        self.rect = self.image.get_rect()
        self.rect[0:2] = pos
        self.speedx = 7
        self.dir_x = 1
        self.direct = self.right
    #Update the boss   
    def update(self):
        #random numbers to determine when to change direction and shoot
        changeMove = randint(0,60)
        shootRand = randint(0,30)
        #if 0, start moving left; if 1, start moving right
        if changeMove == 0:
            self.dir_x= -1
            self.direct = self.left
        elif changeMove == 1:
            self.dir_x = 1
            self.direct = self.right

        #if 0, shoot up; if 1, shoot left; if 2, shoot right
        if shootRand == 0:
            self.direct = self.up
            eMissile_group.add(eMissile((self.rect.topleft),"up"))
            eMissile_group.add(eMissile((self.rect.topright),"up"))
        elif shootRand == 1:
            self.direct = self.left
            eMissile_group.add(eMissile((self.rect.midleft[0],self.rect.midleft[1]-10),"left"))
            eMissile_group.add(eMissile((self.rect.midleft[0],self.rect.midleft[1]+10),"left"))
        elif shootRand == 2:
            self.direct = self.right
            eMissile_group.add(eMissile((self.rect.midright[0],self.rect.midright[1]-10),"right"))
            eMissile_group.add(eMissile((self.rect.midright[0],self.rect.midright[1]+10),"right"))

        #if player laser collides, decrease health 
        if pygame.sprite.groupcollide(bossSprite,missile_group,0,1):
            self.health -= 4
            if self.health == 0:
                #kill the boss when health is 0 and add 2000 to score
                self.kill()
                global newScore
                newScore += 2000
        #if at the edges of screen, reverse direction
        if self.rect.left < 0:
            self.dir_x = 1
            self.direct = self.right
        elif self.rect.right > 898:
            self.dir_x = -1
            self.direct = self.left
        elif self.rect.left == 445:
            bossmoving = False

        #movement of boss
        self.rect.move_ip(self.speedx*self.dir_x,0)

        
class Missile(pygame.sprite.Sprite):
    #initialize the laser sprite 
    def __init__(self,robotpos,state):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("redlaserRay.png") #load image
        self.image = pygame.transform.scale(self.image, (25,25))
        self.image = pygame.transform.rotate(self.image, 90)# rotate image to up/down
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = robotpos
        self.state = state
        if self.state == "right" or self.state == "left": #if the variable is right or left, rotate it back
            self.image = pygame.transform.rotate(self.image, 90)
        
        
    def update(self):
        #edge of screen, destroy laser
        if self.rect.left >1000 or self.rect.right<0 or self.rect.top<0 or self.rect.bottom>1000:
            self.kill()
        else:
            #move in corresponding direction
            if self.state == "up":
                self.rect.move_ip(0,-20)
            elif self.state == "right":
                self.rect.move_ip(20,0)
            elif self.state == "left":
                self.rect.move_ip(-20,0)
            else:
                self.rect.move_ip(0,20)
                
class Enemy2(pygame.sprite.Sprite):
    #initialize sprite
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tanks2.png") #load image
        #initialize lists for blitting different directions
        self.down = []
        self.up = []
        self.right = []
        self.left = []
        self.image.set_colorkey((255,255,255))
        #add up sprites to up list
        for a in range(1,4,1):
            self.pic = self.image.subsurface((117*(a-1),1,117,90))
            self.pic.set_colorkey((255,255,255))
            self.pic.convert_alpha()
            self.pic = pygame.transform.smoothscale(self.pic, (50,50))
            self.up.append(self.pic)
        #other attributes such as the rectangle, position of the image and speed/direction 
        self.image = self.up[0]
        self.rect = self.up[0].get_rect()
        self.rect[0:2] = pos
        self.speedx = 1
        self.dir_x = 1
        self.state = "down"
        
    def update(self,up):
        #if it collides with laser, kill it and add 10 to score
        if pygame.sprite.groupcollide(enemySprites, missile_group, 1, 1):
            global newScore
            newScore += 10
        #if it collides with player, reduce shield/health and kill it
        elif self.rect.colliderect(jesusbot):
            if jesusbot.shield > 0:
                jesusbot.shield -= 1
            else:
                jesusbot.health -= 1
            self.kill()
        #load a random number to determine if to strafe left or right
        randomDirection = randint(0,30)
        if randomDirection == 0:
            self.dir_x = 1
        elif randomDirection == 1:
            self.dir_x = -1
        #blit up animation 
        screen.blit(self.up[up],self.rect)
        if self.rect.left < 1: #if at left edge, reverse direction
            self.dir_x *= -1
        if self.rect.right > 900: #reverse direction
            self.dir_x *= -1
        if self.rect.bottom < 0: #if at top, kill it
            self.kill()
        else: #move up and left/right
            self.rect.move_ip(self.speedx*self.dir_x,-2) 

class Enemy(pygame.sprite.Sprite):
    #initalize sprite
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("tanks3.png") #load image
        self.down = []
        self.up = []
        self.right = []
        self.left = []
        self.image.set_colorkey((255,255,255))
        self.pic = self.image.subsurface((130,3,100,110)) #load part of picture
        self.pic.set_colorkey((255,255,255))
        self.pic.convert_alpha()
        self.pic = pygame.transform.smoothscale(self.pic, (50,50)) #scale it to 50,50 pixels
        #get different attributes
        self.up.append(self.pic)
        self.image = self.up[0]
        self.rect = self.up[0].get_rect()
        self.rect[0:2] = pos
        self.speedx = 1
        self.dir_x = 1
        self.state = "down"
        
    def update(self,up):
        #if laser hits the group, kill it and add score
        if pygame.sprite.groupcollide(enemySprites, missile_group, 1, 1):
            global newScore
            newScore += 10
        #if player collides with enemy, kill it and reduce shield/health
        elif self.rect.colliderect(jesusbot):
            if jesusbot.shield > 0:
                jesusbot.shield -= 1
            else:
                jesusbot.health -= 1
            self.kill()
        #use random number to determine whether to move left or right
        randomDirection = randint(0,30)
        if randomDirection == 0:
            self.dir_x = 1
        elif randomDirection == 1:
            self.dir_x = -1
        #blit up animation
        screen.blit(self.up[0],self.rect)
        if self.rect.left < 1:
            self.dir_x *= -1 #reverse direction at edge
        if self.rect.right > 900:
            self.dir_x *= -1 #reverse direction at edge
        if self.rect.bottom < 0:
            self.kill()
        else: #move up and strafe left/right
            self.rect.move_ip(self.speedx*self.dir_x,-2)
            
class batteryPowerup(pygame.sprite.Sprite):
    #initialize sprite
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("battery.png") #load battery picture
        self.rect = self.image.get_rect()
        self.rect[0:2] = pos #set position of the picture
        self.image.set_colorkey((255,255,255))

    def update(self):
        #if player collects it, delete it and restore health to full
        if self.rect.colliderect(jesusbot):
            jesusbot.health = 5
            self.kill()
        elif self.rect.bottom < 0: #delete if at top of the screen
            self.kill()
        else: #move up
            self.rect.move_ip(0,-4)

class shieldPowerup(pygame.sprite.Sprite):
    #initialize sprite
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("shield.png") #load picture
        self.rect = self.image.get_rect() 
        self.rect[0:2]= pos #set position of the picture
        self.image.set_colorkey((255,255,255))

    def update(self):
        #if player collects it, delete it, give score, and restore/give shield
        if self.rect.colliderect(jesusbot):
            global newScore
            newScore += 100
            jesusbot.shield = 3
            self.kill()
        elif self.rect.left > 900: #if at edge, delete it 
            self.kill()
        else:
            self.rect.move_ip(4,0) #move right

class winePowerup(pygame.sprite.Sprite):
    #initialize sprite
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("wine.png") #load picture
        self.rect = self.image.get_rect()
        self.rect[0:2] = pos #set position of the picture
        self.image.set_colorkey((255,255,255))

    def update(self):
        #if player collects, delete it, give score 
        if self.rect.colliderect(jesusbot):
            global newScore
            newScore += 100
            self.kill()
        elif self.rect.right < 0: #if at edge, delete it
            self.kill()
        else: #move left
            self.rect.move_ip(-4,0)
#------------------------------------------------------------------------

#------------------------Functions--------------------------------------
   
def randomSpawn():
    #use random number and only spawn enemies at certain numbers
    randomSpawn = randint(0,65)
    if randomSpawn == 0:
        enemySprites.add(Enemy2((randint(100,800),530)))
    if randomSpawn == 1:
        enemySprites.add(Enemy((randint(100,800),530)))

def powerupSpawn():
    #use random number and only spawn enemies at certain numbers
    powerupSpawn = randint(0,700)
    if powerupSpawn == 1:
        batterySprites.add(batteryPowerup((randint(100,800),545)))
    elif powerupSpawn == 2:
        shieldSprites.add(shieldPowerup((-50,(randint(100,800)))))
    elif powerupSpawn == 3:
        wineSprites.add(winePowerup((900,(randint(100,400)))))
        
def instructions():
    #blit the different pictures for the instructions
    screen.blit(img, (0,0))
    screen.blit(story, (0,0))
    screen.blit(robot, (600, 180))
    screen.blit(label6,(500,490))
    pygame.display.flip()
#------------------------------------------------------------------------

#-----------------------Initialize Variables-----------------------------

#initialize the labels for the main menu
label = my_font.render("Welcome to JesusBot!!", True, (255,0,0))
label2= my_font2.render("1. Start", False, (0,0, 255))
label3= my_font2.render("2.Help", False, (0,0, 255))
label4= my_font2.render("3.High Score", False, (0,0, 255))
label5= my_font2.render("4.Exit", False, (0,0, 255))
label6= my_font2.render("Back", False, (0,0,255))

#initialize the clock and main loop
clock = pygame.time.Clock()
keep_going = True

#load and play music
pygame.mixer.music.load("The King Of Fighters XIII OST - 02 - Character Select.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
#-------------------------------------------------------------------

#------------------------Main------------------------------------------
    
while keep_going:
    clock.tick(30)
    for ev in pygame.event.get():
        #if user quits, exit loop
        if ev.type == QUIT:
            keep_going = False
        if ev.type == MOUSEMOTION:
            #highlight the different parts of the screen based upon where mouse is
            if pygame.mouse.get_pos()[0] in range(100,307) and pygame.mouse.get_pos()[1] in range(300,350):
                label2 = my_font2.render("1. Start", False, (255,40,90))
            else:
                label2= my_font2.render("1. Start", False, (0,0, 255))
            if pygame.mouse.get_pos()[0] in range(307,472) and pygame.mouse.get_pos()[1] in range(350,400):
                label3= my_font2.render("2.Help", False, (90,140,120))
            else:
                label3= my_font2.render("2.Help", False, (0,0, 255))
            if pygame.mouse.get_pos()[0] in range(472,809) and pygame.mouse.get_pos()[1] in range(400,480):
                label4= my_font2.render("3.High Score", False, (0,200,198))
            else:
                label4= my_font2.render("3.High Score", False, (0,0, 255))
            if pygame.mouse.get_pos()[0] in range(100,260) and pygame.mouse.get_pos()[1] in range(450,510):
                label5= my_font2.render("4.Exit", False, (180,130,200))
            else:
                label5= my_font2.render("4.Exit", False, (0,0,255))
        if ev.type == MOUSEBUTTONDOWN:
            #if player presses start, start the game
            if pygame.mouse.get_pos()[0] in range(100,307) and pygame.mouse.get_pos()[1] in range(300,350):
                #initialize all the necessary variables
                win = False
                timecounter = 0
                running = True
                bossmoving = True
                left = 0
                up = 0
                right = 0
                newScore = 0
                s = 0
                r = 0
                timer = 0
                hitTimer = 0
                myfont = pygame.font.SysFont("Impact", 20)
                clock = pygame.time.Clock()
                count = 0
                jesusbot = Player((446,0)) #player
                #load sprite groups 
                eMissile_group = pygame.sprite.Group()
                missile_group = pygame.sprite.Group()
                enemySprites = pygame.sprite.Group()
                batterySprites = pygame.sprite.Group()
                shieldSprites = pygame.sprite.Group()
                wineSprites = pygame.sprite.Group()
                bossSprite = pygame.sprite.Group()
                #add boss
                boss = Boss((500,375))
                bossSprite.add(boss)
                #load and play music
                pygame.mixer.music.load("Marvel vs. Capcom 3 OST - Theme of Zero Extended.mp3")
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
                
                while running:
                    clock.tick(30)
                    r = count%20
                    r = int(r/5)
                    keys = pygame.key.get_pressed()  #load whether a key is pressed into a variable
                    if keys[K_UP]:
                        jesusbot.dy = -10 #if up is pressed, blit up animation and move the player up
                        screen.blit(jesusbot.up[r],jesusbot.rect)
                    elif keys[K_RIGHT]:
                        jesusbot.dx = 10 #if right is pressed, blit right animation, move right
                        screen.blit(jesusbot.right[r],jesusbot.rect)
                    elif keys[K_LEFT]:
                        jesusbot.dx = -10 #if left is pressed, blit left animation, move left
                        screen.blit(jesusbot.left[r],jesusbot.rect)
                    elif keys[K_DOWN]:
                        jesusbot.dy = 10 #if down is pressed, blit down animation, move down
                        screen.blit(jesusbot.down[r],jesusbot.rect)
                    else: #otherwise just blit still animation
                        screen.blit(jesusbot.down[0],jesusbot.rect)
        
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            #if someone quits, exit loops
                            running = False
                            keep_going = False
                        elif event.type == pygame.KEYUP: #if player releases key, stop movement
                            if event.key == K_LEFT:
                                jesusbot.dx = 0
                            elif event.key == K_RIGHT:
                                jesusbot.dx = 0
                            elif event.key == K_UP:
                                jesusbot.dy = 0
                            elif event.key == K_DOWN:
                                jesusbot.dy = 0
                                
                    #uses a variable to determine a variable to blit the enemy2 animation
                    if count % 4 == 0:
                            up += 1
                            if up == 3:
                                up = 0
                
                    if jesusbot.health == 0:
                        running = False #if player dies, loop is false and quit to main menu
                    else: #otherwise, just blit the health and shield bars
                        pygame.draw.rect(screen,(0,255,0),(10,30,((jesusbot.health*20)),16))
                        pygame.draw.rect(screen,(0,0,255),(10,72,((jesusbot.shield*33)),16))

                    #load the different labels and then blit them(health,shield,score)
                    score = myfont.render("Score:",True,(0,0,0))
                    playerScore = myfont.render(str(newScore),True,(0,0,0))
                    playerHealth = myfont.render("Health:",True,(0,0,0))
                    playerShield = myfont.render("Shield:",True,(0,0,0))
                    screen.blit(score, (800, 6))
                    screen.blit(playerScore, (800,28))
                    screen.blit(playerHealth,(10,6))
                    screen.blit(playerShield,(10,46))

                    #use random spawn functions for powerups and enemys
                    powerupSpawn()
                    randomSpawn()

                    #clear the pictures of the groups before updating and drawing new enemies
                    enemySprites.clear(screen,ground)
                    missile_group.clear(screen,ground)
                    batterySprites.clear(screen,ground)
                    shieldSprites.clear(screen,ground)
                    wineSprites.clear(screen,ground)

                    #use the update functions inside of the classes and respective groups
                    jesusbot.update()
                    enemySprites.update(up)
                    batterySprites.update()
                    shieldSprites.update()
                    wineSprites.update()
                    missile_group.update()

                    #blit the entire group
                    batterySprites.draw(screen)
                    shieldSprites.draw(screen)
                    wineSprites.draw(screen)
                    missile_group.draw(screen)
                    count += 1
                    pygame.display.flip()
                    screen.blit(ground,(0,0)) #blit the background
                    timecounter += 1
                    if timecounter == 1000: #when timer is 1000, exit loop
                        running = False
                if keep_going and timecounter == 1000:
                    #load and play music
                    pygame.mixer.music.load("1.mp3")
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(-1)
                    while timecounter < 1500:
                        #for a few seconds, blit the "get ready" picture and empty out all the recent enemies
                        screen.blit(img,(0,0))
                        phrasefont = pygame.font.Font("weird_science_nbp.ttf", 30)
                        bbattle = phrasefont.render("Get ready for the final battle!",False,(233,24,100))
                        screen.blit(bbattle,(0,200))
                        pygame.display.flip()
                        #increment the time counter so that it will eventually stop showing the picture and move on
                        timecounter += 1
                        enemySprites.empty()
                        batterySprites.empty()
                        shieldSprites.empty()
                        wineSprites.empty()
                        missile_group.empty()
                        jesusbot.rect[0:2] = [446,0] #reset player position
                if keep_going: #boss battle
                    running = True
                    while running:
                        clock.tick(30)
                        keys = pygame.key.get_pressed()
                        r = count%20
                        r = int(r/5)
                        keys = pygame.key.get_pressed()  
                        if keys[K_UP]:
                            jesusbot.dy = -10 #move up and up animation
                            screen.blit(jesusbot.up[r],jesusbot.rect)
                        elif keys[K_RIGHT]:
                            jesusbot.dx = 10 #move right and right animation
                            screen.blit(jesusbot.right[r],jesusbot.rect)
                        elif keys[K_LEFT]:
                            jesusbot.dx = -10 #move left and left animation
                            screen.blit(jesusbot.left[r],jesusbot.rect)
                        elif keys[K_DOWN]:
                            jesusbot.dy = 10 #move down and down animation
                            screen.blit(jesusbot.down[r],jesusbot.rect)
                        else: #still animation
                            screen.blit(jesusbot.down[0],jesusbot.rect)
                            
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                running = False
                                keep_going = False
                            elif event.type == pygame.KEYUP: #if player releases the key, stop all movement
                                if event.key == K_LEFT:
                                    jesusbot.dx = 0
                                elif event.key == K_RIGHT:
                                    jesusbot.dx = 0
                                elif event.key == K_UP:
                                    jesusbot.dy = 0
                                elif event.key == K_DOWN:
                                    jesusbot.dy = 0

                        #uses variable count to determine the animation variable to animate the enemy2            
                        if count % 4 == 0:
                                up += 1
                                if up == 3:
                                    up = 0

                        #if the boss is in movement and isn't dead, blit the animation             
                        if bossmoving and boss.health > 0:
                            screen.blit(boss.direct[s],boss.rect)
                            if count % 4 == 0: #variable to determine which picture to blit so it animates
                                s += 1
                                if s == 4: #if it's past the list of the boss, reset it back to 0
                                    s = 0
                                    
                        if jesusbot.health <= 0: #if player dies, exit loop
                            running = False
                        else: #draw health and shield bars
                            pygame.draw.rect(screen,(0,255,0),(10,30,((jesusbot.health*20)),16))
                            pygame.draw.rect(screen,(0,0,255),(10,72,((jesusbot.shield*33)),16))


                        if boss.health > 0: #as long as boss as health, draw its health bar
                            pygame.draw.rect(screen,(255,0,0),(10,114,((boss.health*1)),16))
                        elif boss.health == 0: #if boss health is 0, end loop and start new one
                            running = False
                            win = True

                        if boss.rect.colliderect(jesusbot) and hitTimer == 0: #if player collides with boss, reset hitTimer to 60 so you won't be hit again
                            hitTimer = 60
                            if jesusbot.shield > 0: #reduce shield/health 
                                jesusbot.shield -= 1
                            else:
                                jesusbot.health -= 1

                        if hitTimer > 0: #reduce the hitTimer with boss by 1
                            hitTimer -= 1
                        #initialize labels for score,health,shield and then blit them
                        score = myfont.render("Score:",True,(255,255,255))
                        playerScore = myfont.render(str(newScore),True,(255,255,255))
                        playerHealth = myfont.render("Health:",True,(255,255,255))
                        playerShield = myfont.render("Shield:",True,(255,255,255))
                        bossHealth = myfont.render("Boss HP:",True,(255,255,255))
                        screen.blit(score, (800, 6))
                        screen.blit(playerScore, (800,28))
                        screen.blit(playerHealth,(10,6))
                        screen.blit(playerShield,(10,46))
                        screen.blit(bossHealth, (10,88))

                        #random power up spawns and enemy spawns
                        powerupSpawn()
                        randomSpawn()

                        #clears the group of drawings of each group on the screen so it doesn't remain on the screen             
                        enemySprites.clear(screen,ground2)
                        bossSprite.clear(screen,ground2)
                        missile_group.clear(screen,ground2)
                        eMissile_group.clear(screen,ground2)
                        batterySprites.clear(screen,ground2)
                        shieldSprites.clear(screen,ground2)
                        wineSprites.clear(screen,ground2)

                        #update functions for each group/sprite
                        jesusbot.update()
                        enemySprites.update(up)         
                        bossSprite.update()
                        batterySprites.update()
                        shieldSprites.update()
                        wineSprites.update()
                        missile_group.update()
                        eMissile_group.update()

                        #blit the sprites
                        batterySprites.draw(screen)
                        shieldSprites.draw(screen)
                        wineSprites.draw(screen)
                        missile_group.draw(screen)
                        eMissile_group.draw(screen)
                        count += 1
                        pygame.display.flip()
                        screen.blit(ground2,(0,0)) #blit new background                    
                if keep_going:
                    #initialize text box to enter name 
                    field_surf = pygame.Surface((300, 50)).convert()
                    field_surf.fill((255,255,255)) #Creates white text box
                    namefont = pygame.font.SysFont("helvetica", 20)
                    phrasefont = pygame.font.Font("Pixel LCD-7.ttf", 30) #sets fonts
                    field_value = "" #the textbox is empty
                    field = namefont.render(field_value, True, (0,0,0))
                    running = True
                    while running:
                        clock.tick(30)
                        for ev in pygame.event.get():
                            if ev.type == QUIT:
                                running = False
                                keep_going = False #will exit entire program if exitted
                            elif ev.type == KEYDOWN:
                                if ev.key == K_BACKSPACE and len(field_value)>0:
                                    field_value = field_value[:-1] #deletes a character with backspace
                                elif (ev.unicode.isalnum() or ev.key==K_SPACE) and len(field_value) < 10:
                                    field_value += ev.unicode #adds characters that ar typed in (max 10)
                                field = namefont.render(field_value,True,(0,0,0)) #rendered again
                                if ev.key == K_RETURN: #when enter is pressed
                                    running = False
                                    #writes the name and score and saves it to the text file
                                    namefile = open("names.txt", "a")
                                    namestring = '\n' + field_value
                                    namefile.write(namestring)
                                    namefile.close()
                                    scorefile = open("score.txt", "a")
                                    scorestring = '\n' + str(newScore)
                                    scorefile.write(scorestring)
                                    scorefile.close()
                        screen.blit(img, (0,0))
                        if win:
                            over = highscoretitlefont.render("You Win!",False,(50,110,160))
                        else:
                            over = highscoretitlefont.render("Game Over!",False,(50,110,160)) #different phrases are shown depending if the boss was beaten
                        phrase = phrasefont.render("Enter your name and press 'Enter':",False, (30,70,110))
                        screen.blit(over, (200,20))
                        screen.blit(phrase, (100,200))
                        screen.blit(field_surf, (300,400))
                        screen.blit(field, (310,415))
                        pygame.display.flip() #displays everything onscreen
                    pygame.mixer.music.load("The King Of Fighters XIII OST - 02 - Character Select.mp3")
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(-1)
            if pygame.mouse.get_pos()[0] in range(307,472) and pygame.mouse.get_pos()[1] in range(350,400):
                #displays instructions
                run = True
                while run:
                    instructions()
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            run = False
                            keep_going = False
                        if event.type == MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pos()[0] in range(500,660) and pygame.mouse.get_pos()[1] in range(490,550):
                                run = False
                        if event.type == MOUSEMOTION:
                            if pygame.mouse.get_pos()[0] in range(500,660) and pygame.mouse.get_pos()[1] in range(490,550):
                                label6= my_font2.render("Back", False, (70,150,55))
                            else:
                                label6= my_font2.render("Back", False, (0,0,255))
            if pygame.mouse.get_pos()[0] in range(472,809) and pygame.mouse.get_pos()[1] in range(400,480):
                #reads text files and displays the top 7 scores and corresponding names
                run2 = True
                readfile = open("names.txt", "r")
                names = readfile.read()
                readfile.close()
                names = names.split("\n")
                fi = open("score.txt", "r")
                scores = fi.read()
                fi.close()
                scores = scores.split("\n")
                highscore = []
                for x in range(len(names)):
                    sublist = [names[x],int(scores[x])]
                    highscore.append(sublist)
                highscore.sort(lambda a,b: b[1]-a[1]) #sorts the list from greatest to least
                screen.blit(img, (0,0))
                highscorecount = 0
                for x in highscore:
                    #after the first (top) 7, it will stop rendering
                    if highscorecount < 7:
                        string = str(highscore.index(x)+1) + ")    " + x[0] + ":" + str(x[1])
                        scoredisplay = highscorefont.render(string, False, (60,200,70))
                        screen.blit(scoredisplay, (0, (highscore.index(x)+2) * 50))
                        highscorecount += 1
                color = 0
                while run2:
                    if color % 100 in range(0,51):
                        highscore_title = highscoretitlefont.render("Highscores!",False,(90,190,160))
                    else:
                        highscore_title = highscoretitlefont.render("Highscores!",False,(150,100,150))
                    color = color + 1 #alternates colors for the title so it looks like it's flashing
                    screen.blit(highscore_title,(0,0))
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            run2 = False
                            keep_going = False
                        if event.type == MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pos()[0] in range(500,660) and pygame.mouse.get_pos()[1] in range(490,550):
                                run2 = False
                        if event.type == MOUSEMOTION:
                            if pygame.mouse.get_pos()[0] in range(500,660) and pygame.mouse.get_pos()[1] in range(490,550):
                                label6= my_font2.render("Back", False, (70,150,55))
                            else:
                                label6= my_font2.render("Back", False, (0,0,255))
                    screen.blit(label6, (500,490))
                    pygame.display.flip()
            if pygame.mouse.get_pos()[0] in range(100,260) and pygame.mouse.get_pos()[1] in range(450,510):
                keep_going = False
    screen.blit(img, (0,0))
    screen.blit(label,(10,30))
    screen.blit(label2,(100,300))
    screen.blit(label3,(307,350))
    screen.blit(label4,(472,400))
    screen.blit(label5,(100,450))
    pygame.display.flip()
pygame.quit()
