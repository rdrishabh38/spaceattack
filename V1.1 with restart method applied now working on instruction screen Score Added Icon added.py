# 1 - Import library
import pygame
from pygame.locals import *
import math
import random #line 5
import pygame.mixer
import sys
import time

# 2 - Initialize the game
pygame.init()
# initialize the t0 variable, "starting the stopwatch"
t0 = time.time()
Intro_clock=pygame.time.Clock()
width, height = 640, 452
screen=pygame.display.set_mode((width, height))#game window resolution
pygame.display.set_caption('Space Attack')
keys = [False, False] #move right and left in the same order

FPS=100

white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
rCBack = ( 27, 27, 27 )
No_of_Flakes=10
font = pygame.font.Font("SpaceRes/font.ttf", 24)
icon=pygame.image.load("SpaceRes/Images/ship.png")
pygame.display.set_icon(icon)



pygame.mixer.init()
# 3 - Load images
player = pygame.image.load("SpaceRes/Images/ship.png")
background = pygame.image.load("SpaceRes/Images/spacebackground.jpg")
arrow = pygame.image.load("SpaceRes/Images/bulletcropped.png")
#badguyimg1 = pygame.image.load("SpaceRes/Images/eship1.png")
badguyimg2 = pygame.image.load("SpaceRes/Images/eship2.png")
#badguyimg3 = pygame.image.load("SpaceRes/Images/eship3.png")
#badguyimg4 = pygame.image.load("SpaceRes/Images/eship4.png")
healthbar = pygame.image.load("SpaceRes/Images/healthbar.png")
health = pygame.image.load("SpaceRes/Images/health.png")
gameover = pygame.image.load("SpaceRes/Images/gameover.png")
youwin = pygame.image.load("SpaceRes/Images/youwin.png")

#Music Section
# 3.1 - Load audio
hit = pygame.mixer.Sound("SpaceRes/audio/explode.wav")
enemy = pygame.mixer.Sound("SpaceRes/audio/enemy.wav")
shoot = pygame.mixer.Sound("SpaceRes/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('SpaceRes/audio/boss.xm')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(1.0)


def score (score):
##    score_text=font.render("Score: ")+str(score),True, green
##    screen.blit(score_text,[0,30])
    
    score_text = font.render("Score :"+str(score).zfill(2), True, white)
    score_Rect = score_text.get_rect()
    score_Rect.topleft=[0,30]
    screen.blit(score_text, score_Rect)



def pause():
    paused = True
    while paused:
        t2=time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:          
                    pygame.quit()
                    sys.exit()
        screen.fill(rCBack)
        Replay("Paused",green,height/2)
        Replay("Press C to resume or Q to quit",green,height/1.75)
        pygame.display.update()
        Intro_clock.tick(5)
    
def intro_screen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    GameExit= True
                    GameOver= False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_c:
                    GameExit=False
                    intro=False
                    gameloop()
                if event.key == pygame.K_p:
                    pause()
        
        screen.fill(rCBack)
        Replay("Welcome to Space Attack !",green,height/8)

        Replay("The objective of the game is to survive the",green,height/4)


        Replay("waves of Enemy Spaceships.",green,height/3.2)

        
        
        Replay("The wave timer is 90 seconds.",green,height/2.2)

        Replay("Press A/D to move Left/Right respectively.",green,height/1.7)
        Replay("Press either mouse buttons to fire bullets",green,height/1.5)
        Replay("from your own spaceship.",green,height/1.35)
        Replay("Press C to play,P to Pause or Q to quit.",green,height/1.1)

        pygame.display.update()
        Intro_clock.tick(15)
def Message_to_Screen(exitcode,accuracy,score1):
    # 11 - Win/lose display        
    if exitcode==0: #when time elapsed is less than 90 seconds i.e healthvalue=0
        pygame.font.init()
##        font = pygame.font.Font("font.ttf", 24)
        text = font.render("Accuracy: "+str(accuracy)+"% Score :"+str(score1), True, red)
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+24
        screen.blit(gameover, (0,0))
        screen.blit(text, textRect)
##        print("message to screen executed")
        
    else:
        #this loop executes when exitcode=1 i.e time elapsed > 90 seconds
        pygame.font.init()
##        font = pygame.font.Font("font.ttf", 24)
        text = font.render("Accuracy: "+str(accuracy)+"% Score :"+str(score1), True, green)
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+24
        screen.blit(youwin, (0,0))
        screen.blit(text, textRect)
##        print("message to screen executed") 
       
def Replay(msg,color,h):
    screen_text = font.render(msg, True , color)
    screen.blit(screen_text, [0,h])


# 4 - keep looping through
def gameloop():
    # initialize the t0 variable, "starting the stopwatch"
    t0 = time.time()
    playerpos=[320,390] #variable to track position of player
    acc=[0,0] #accuracy calculator 0-total bullets fired 1-bullets hit
    arrows=[]
    badtimer=100
    badtimer1=0
    badguys=[[0,100]]
    healthvalue=200 #line 18
    Off_Screen_Enemy_Spaceship_Counter=0
    Enemy_Spaceship_Arrow_Hit_Counter=0
    Bullet_Pop_Off_Screen_Counter=0
    Badrect_Colliderect_Playerrect_Counter=0
    snow_flakes_list = []
    loc_x, loc_y = 0, 0
    num=0
    zz=1
    score1=0
    clock=pygame.time.Clock()
    GameExit = False #before it was running = 1
    GameOver = False
    exitcode = 0
    while not GameExit:
        # calculate the time since some reference point (here the Unix Epoch)
        t1 = time.time()
        dt=t1-t0
        badtimer-=1
        clock.tick(FPS)
        # 5 - clear the screen before drawing it again
        screen.fill(0)
        # 6 - draw the screen elements
        screen.blit(background, (0,0))
        # 6.1 - Set player position and rotation
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
        playerrot = pygame.transform.rotate(player, 360-angle*57.29)
        playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
        screen.blit(player, playerpos)
        #snowfall attempt
        if zz==1:
##            num+=1
##            print num," times loop running"
            for i in range(No_of_Flakes ):
                    loc_x = random.randrange( 0, width )
                    loc_y = random.randrange( 0, height )
                    snow_flakes_list.append( [ loc_x, loc_y ] )
                    zz+=1
        if dt<=90:
            for i in range( len( snow_flakes_list ) ):
                        pygame.draw.circle( screen, white, snow_flakes_list[i], random.choice( [2, 3, 4] ) )
                        snow_flakes_list[i][1] += 1
                        
                        if snow_flakes_list[i][1] > height:
                            snow_flakes_list[i][1] = random.randrange( -30, -20 )
                            snow_flakes_list[i][0] = random.randrange( 0, width )
                            #snowfall ended
        # 6.2 - Draw arrows
        for bullet in arrows:
            index=0
            velx=math.cos(bullet[0])*4
            vely=math.sin(bullet[0])*4
            bullet[1]+=velx
            bullet[2]+=vely
            if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
                arrows.pop(index)
##                Bullet_Pop_Off_Screen_Counter+=1
##                print "bullet pop off screen"
##                print Bullet_Pop_Off_Screen_Counter
                
            index+=1
            for projectile in arrows:
                arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
                screen.blit(arrow, (projectile[1], projectile[2]))
        # 6.3 - Draw enemy space ships
        if badtimer==0:
            badguys.append([random.randint(20,620),0])
            badtimer=100-(badtimer1*2)
            if badtimer1>=35:
                badtimer1=35
            else:
                badtimer1+=5
        index=0
        for badguy in badguys:
            if badguy[1]>480:
                badguys.pop(index)
##                Off_Screen_Enemy_Spaceship_Counter+=1
##                print "Enemy Spaceship pop from bottom screen"
##                print Off_Screen_Enemy_Spaceship_Counter
            badguy[1]+=3 #speed of enemy space ships change 3 to others to hf
            # 6.3.1 - Attack player spaceship
            # 6.3.1 - Attack castle
            badrect=pygame.Rect(badguyimg2.get_rect())
            playerrect=pygame.Rect(player.get_rect())
            badrect.top=badguy[1]
            badrect.left=badguy[0]
            playerrect.top=playerpos[1]
            playerrect.left=playerpos[0]
            if badrect.colliderect(playerrect):
                hit.play()
                #pygame.draw.rect(screen,white,playerrect)
                healthvalue -=20
##                print healthvalue
##                Badrect_Colliderect_Playerrect_Counter+=1
##                print "Collision of Badrect_Colliderect_Playerrect"
##                print Badrect_Colliderect_Playerrect_Counter
                badguys.pop(index)
            #6.3.2 - Check for collisions
            index1=0
            for bullet in arrows:
                bullrect=pygame.Rect(arrow.get_rect())
                bullrect.left=bullet[1]
                bullrect.top=bullet[2]
                if badrect.colliderect(bullrect):
                    enemy.play()
                    acc[0]+=1
                    score1+=1
                    badguys.pop(index)
##                    Enemy_Spaceship_Arrow_Hit_Counter+=1
##                    print "Bullet Hit so Enemy Spaceship and arrow popped"
##                    print Enemy_Spaceship_Arrow_Hit_Counter
                    arrows.pop(index1)
                index1+=1
            badrect=pygame.Rect(badguyimg2.get_rect())
            # next bad guy
            index+=1
        for badguy in badguys:
            #screen.blit(badguyimg1, badguy)#unable to use different spaceships now.
            screen.blit(badguyimg2, badguy)#will try later :/
        # 6.4 - Draw clock
        if dt>60:
            survivedtext = font.render(str(int((dt)/60))+":"+str(int(dt-60)).zfill(2), True, white)
            textRect = survivedtext.get_rect()
            textRect.topright=[635,5]
            screen.blit(survivedtext, textRect)

        if dt<60:
            survivedtext = font.render(str(0)+":"+str(int(dt)).zfill(2), True, white)
            textRect = survivedtext.get_rect()
            textRect.topright=[635,5]
            screen.blit(survivedtext, textRect)

        # 6.5 - Draw health bar
        screen.blit(healthbar, (5,5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1+8,8))
    ##    snowfallasreqedit.main()
        # 7 - update the screen
        score(score1)
        pygame.display.flip()
        # 8 - loop through the events
        for event in pygame.event.get():
            # check if the event is the X button 
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit() 
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==K_a:
                    keys[0]=True
                elif event.key==K_d:
                    keys[1]=True
                elif event.key==K_p:
                    pause()
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_a:
                    keys[0]=False
                elif event.key==pygame.K_d:
                    keys[1]=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                shoot.play()
                position=pygame.mouse.get_pos()
                acc[1]+=1
                arrows.append([math.atan2(position[1]-(playerpos1[1]),position[0]-(playerpos1[0])),playerpos1[0]+60,playerpos1[1]+32])
        if keys[0]:
            playerpos[0]-=4
        elif keys[1]:
            playerpos[0]+=4
        if playerpos[0]>590: #check for right boundary
            playerpos[0]=590
        if playerpos[0]<0: #check for left boundary
            playerpos[0]=0

        #10 - Win/Lose check
        if dt>=90:
            GameExit= True
            GameOver= True
            t0=t1 #reset game timer.
            exitcode=1
        if healthvalue<=0:
            GameExit= True
            GameOver= True
            exitcode=0
            t0=t1 #reset game timer.
        if acc[1]!=0:
            accuracy=acc[0]*1.0/acc[1]*100
        else:
            accuracy=0

    while GameOver == True:
        screen.fill(rCBack)
        Message_to_Screen(exitcode,accuracy,score1)
        h=height/1.75
        if exitcode==0:
            Replay("Game Over. Press C to play again or Q to quit",red,h)
        else:
            Replay("Game Over. Press C to play again or Q to quit",green,h)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    GameExit= True
                    GameOver= False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_c:
                    GameExit=False
                    gameloop()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

intro_screen()
gameloop()
