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
width, height = 640, 480
screen=pygame.display.set_mode((width, height), pygame.FULLSCREEN)#game window resolution
pygame.display.set_caption('Space Attack')
keys = [False] #mouse button down for shooting

FPS=60
score1 = 0
level_counter = 0
white=(255,255,255)
red=(200,0,0)
light_red=(255,0,0)
dark_green=(34,177,76)
green = (0,255,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
rCBack = ( 27, 27, 27 )
No_of_Flakes=10
font = pygame.font.Font("SpaceRes/font.ttf", 20)
icon=pygame.image.load("SpaceRes/Images/ship.png").convert_alpha()
pygame.display.set_icon(icon)



pygame.mixer.init()
# 3 - Load images
player = pygame.image.load("SpaceRes/Images/ship.png").convert_alpha()
background = pygame.image.load("SpaceRes/Images/spacebackground.jpg").convert_alpha()
arrow = pygame.image.load("SpaceRes/Images/bulletcropped.png").convert_alpha()
##badguyimg1 = pygame.image.load("SpaceRes/Images/eship1.png")
badguyimg2 = pygame.image.load("SpaceRes/Images/eship2.png").convert_alpha()
##badguyimg3 = pygame.image.load("SpaceRes/Images/eship3.png")
##badguyimg4 = pygame.image.load("SpaceRes/Images/eship4.png")
healthbar = pygame.image.load("SpaceRes/Images/healthbar.png").convert_alpha()
health = pygame.image.load("SpaceRes/Images/health.png").convert_alpha()
gameover = pygame.image.load("SpaceRes/Images/gameover.png").convert_alpha()
youwin = pygame.image.load("SpaceRes/Images/youwin.png").convert_alpha()
explosion = pygame.image.load( "SpaceRes/Images/BombExploding1.png" ).convert_alpha()
exp = pygame.image.load( "SpaceRes/Images/exp.png" ).convert_alpha()
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



#module for explosion
##def sprite( w, h,badguy_x,badguy_y ):
##    animation_frames = []
####    timer = pygame.time.Clock()
####    screen = pygame.display.set_mode( ( 200, 200 ), 0, 32 )
##    width, height = explosion.get_size()
##
##    for i in range( int( width / w ) ):
##        animation_frames.append( explosion.subsurface( ( i * w, 0, w, h ) ) )
##    counter = 0
##
####    while True:
####        for event in pygame.event.get():
####            if event.type == QUIT or ( event.type == KEYDOWN and evt.key == K_ESCAPE ) :
####                pygame.quit()
####                sys.exit()
##
####        screen.fill( ( 27, 27, 27 ) )
##    screen.blit( animation_frames[counter], ( badguy_x, badguy_y-32 ) )
##    counter = ( counter + 1 ) % 6
##    pygame.display.update()
####    Intro_clock.tick(1)
##    ##    timer.tick( FPS )


def sprite( w, h,badguy_x,badguy_y ):
    animation_frames = []
    
    width, height = exp.get_size()

    for i in range( int( width / w ) ):
        animation_frames.append( exp.subsurface( ( i * w, 0, w, h ) ) )
    counter = 0

##    while True:
##        for evt in pygame.event.get():
##            if evt.type == QUIT or ( evt.type == KEYDOWN and evt.key == K_ESCAPE ) :
##                pygame.quit()
##                sys.exit()
    screen.blit( animation_frames[counter], ( badguy_x-50, badguy_y-64 ) )
    counter = ( counter + 1 ) % 35
    pygame.display.update()
##    Intro_clock.tick(1)


##Show how to use exceptions to save a high score for a game.
## 
##Sample Python/Pygame Programs
##Simpson College Computer Science
##http://programarcadegames.com/
##http://simpson.edu/computer-science/

def get_high_score():
    # Default high score
    high_score = 0
 
    # Try to read the high score from a file
    try:
        high_score_file = open("SpaceRes/high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
##        print("The high score is", high_score)
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")
 
    return high_score
 
 
def save_high_score(new_high_score):
    try:
        # Write the file to disk
        high_score_file = open("SpaceRes/high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")
 
def score (score):
##    score_text=font.render("Score: ")+str(score),True, green
##    screen.blit(score_text,[0,30])
    
    score_text = font.render("Score :"+str(int(score)).zfill(2), True, white)
    score_Rect = score_text.get_rect()
    score_Rect.topleft=[0,30]
    screen.blit(score_text, score_Rect)


def difficulty_option():
    difficulty_selected = True      
    while difficulty_selected:
        screen.fill(rCBack)
        Replay("            Choose Difficulty Setting",green,height/3)
        button("Easy",100,250,100,50,dark_green,green,action="Easy")
        button("Medium",250,250,100,50,yellow,light_yellow,action = "Medium")
        button("Hard",400,250,100,50,red,light_red,action = "Hard")
        pygame.display.update()
        Intro_clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def Credits():
    boole = True
    while boole:
        screen.fill(rCBack)
        Replay("This game is created by Rishabh Dixit.",green,height/4)
        Replay("Programmed in Python 2.7 with Pygame Libraries.",green,height/3.2)
        Replay("Thanks for playing !",green,height/1.5)
        Replay("Would love to have response at rdrishabh38@gmail.com",green,height/2.2)
        button("Play",100,380,100,50,dark_green,green,action="Play")
##        button("Controls",250,380,100,50,yellow,light_yellow,action = "Controls")
        button("Quit",400,380,100,50,red,light_red,action = "Quit")
        pygame.display.update()
        Intro_clock.tick(15)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()





    
def text_to_button(msg, color,buttonx,buttony,buttonwidth,buttonheight):
    text=font.render(msg.zfill(2),True,rCBack)
    text_rect = text.get_rect()
    text_rect.center = ((buttonx+(buttonwidth/2)),buttony+(buttonheight/2))
    screen.blit(text,text_rect)

def button(text,x,y,width,height,inactive_color,active_color,action= None):
    global level_counter
    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+width>cursor[0]>x and y+height>cursor[1]>y:
        pygame.draw.rect(screen, active_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "Quit":
                pygame.quit()
                sys.exit()
            if action == "Controls":
                game_controls()
            if action == "Play":
                difficulty_option()
            if action == "Easy":
                level_display_screen(level_counter)
##                print ("easy executed")
                gameloop(20)
            if action == "Medium":
                level_display_screen(level_counter)
##                print ("medium executed")
                gameloop(40)
            if action == "Hard":
                level_display_screen( level_counter)
                gameloop(100)
##                print "hard executed"
##                gameloop()
            if action == "Resume":
                return 1
            if action == "Credits":
                Credits()
    else:
        pygame.draw.rect(screen, inactive_color, (x,y,width,height))

    text_to_button(text,rCBack,x,y,width,height)


def game_controls():
##    clock=pygame.time.Clock()
    gcont = True
    screen.fill(rCBack)
    Replay("Welcome to Space Attack !",green,height/8)
    Replay("Press 'P' to Pause the game anytime.",green,height/3)
    Replay("Press 'F' to toggle fullscreen and window mode.",green,height/2.5)
    Replay("Use mouse to move Left/Right respectively.",green,height/2)
    Replay("Hold either mouse buttons to fire bullets",green,height/1.75)
    Replay("from your own spaceship.",green,height/1.55)
    while gcont:
        button("Play",100,380,100,50,dark_green,green,action="Play")
        button("Quit",400,380,100,50,red,light_red,action = "Quit")
        pygame.display.update()
        Intro_clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def pause():
    paused = True
    clock = pygame.time.Clock()
##    gameloop
    t2=clock.tick()
    screen.fill(rCBack)
    Replay("                    Game Paused",green,height/2)
    pygame.display.update()
    while paused:
##        gameloop.time.sleep(10)
##        t2=time.time()
        button("Resume",100,380,100,50,dark_green,green,action="Resume")
        button("Quit",400,380,100,50,red,light_red,action = "Quit")
        if (button("Resume",100,380,100,50,dark_green,green,action="Resume")):
            paused = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
##            if event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_c:
##                    paused = False
##                elif event.key == pygame.K_q:          
##                    pygame.quit()
##                    sys.exit()
        pygame.display.update()                    
        Intro_clock.tick(20)
        if paused == False:
            t3= clock.tick()
##            t4= t2-t3
            t4 = clock.get_time()
##            print t4
            return t4
            
    
def intro_screen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_q:
##                    GameExit= True
##                    GameOver= False
##                    pygame.quit()
##                    sys.exit()
##                if event.key == pygame.K_c:
##                    GameExit=False
##                    intro=False
##                    gameloop()
                if event.key == pygame.K_p:
                    pause()
        
        screen.fill(rCBack)
        Replay("Welcome to Space Attack !",green,height/8)

        Replay("The objective of the game is to survive the",green,height/4)


        Replay("waves of Enemy Spaceships.",green,height/3.2)

        
        
        Replay("The wave timer is 90 seconds.",green,height/2.2)

##        Replay("Press A/D to move Left/Right respectively.",green,height/1.7)
##        Replay("Press either mouse buttons to fire bullets",green,height/1.5)
##        Replay("from your own spaceship.",green,height/1.35)
##        Replay("Press C to play,P to Pause or Q to quit.",green,height/1.1)

##        cursor = pygame.mouse.get_pos()
##        if 100+100>cursor[0]>100 and 380+50>cursor[1]>380:
##            pygame.draw.rect(screen,green,(100,380,100,50))
##        else:
##            pygame.draw.rect(screen,dark_green,(100,380,100,50))
##        pygame.draw.rect(screen,yellow,(245,380,110,50))
##        pygame.draw.rect(screen,red,(400,380,100,50))
        button("Credits",535,5,100,50,yellow,light_yellow,action = "Credits")
        button("Play",100,380,100,50,dark_green,green,action="Play")
        button("Controls",250,380,100,50,yellow,light_yellow,action = "Controls")
        button("Quit",400,380,100,50,red,light_red,action = "Quit")

        pygame.display.update()
        Intro_clock.tick(15)


##def level(level_number,badguy,index):
##    if level_number == 1:
##        badguy[1]+=3
##    elif level_number == 2:
##        if (((index)%3)==0):
##                badguy [1]+= 7
##        else:
##            badguy[1]+=3
##
##    elif level_number == 3:
##        if (((index)%3)==0):
##                badguy [1]+= 7
##                badguy [0]+= 2
##        else:
##            badguy[1]+=3
##            badguy [0]-=2
##    return 0
    



def Message_to_Screen(exitcode,accuracy,score1,counter):
    # 11 - Win/lose display
    global level_counter
    current_score = int (score1)
    if exitcode==0: #when time elapsed is less than 90 seconds i.e healthvalue=0
        pygame.font.init()
##        font = pygame.font.Font("font.ttf", 24)
        text = font.render("Accuracy: "+str(accuracy)+"% Score :"+str(current_score), True, red)
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+24
        screen.blit(gameover, (0,0))
        screen.blit(text, textRect)

        high_score = get_high_score()
        # Get the score from the current game
        hscore = font.render("All Time High Score: "+str(high_score), True, red)
        hscoreRect = hscore.get_rect()
        hscoreRect.centerx = screen.get_rect().centerx
        hscoreRect.centery = screen.get_rect().centery+60
        screen.blit(hscore,hscoreRect)
        # See if we have a new high score
        if current_score > high_score:
        # We do! Save to disk
##            print("Yea! New high score!")
            save_high_score(current_score)
##                counter = False
##                print counter
                
                
             
##            else:
##                print("Better luck next time.")
##                counter = False
##                print counter
##                Replay("High Score: " +str(high_score),red,height/1.75)
##        print("message to screen executed")
        
    else:
        if level_counter != 30:
            #this loop executes when exitcode=1 i.e time elapsed > 90 seconds
            pygame.font.init()
    ##        font = pygame.font.Font("font.ttf", 24)
            counter = True
            text = font.render("Accuracy: "+str(accuracy)+"% Score :"+str(current_score), True, green)
            textRect = text.get_rect()
            textRect.centerx = screen.get_rect().centerx
            textRect.centery = screen.get_rect().centery+24
            screen.blit(youwin, (0,0))
            screen.blit(text, textRect)


            high_score = get_high_score()
            hscore = font.render("All Time High Score: "+str(high_score), True, green)
            hscoreRect = hscore.get_rect()
            hscoreRect.centerx = screen.get_rect().centerx
            hscoreRect.centery = screen.get_rect().centery+60
            screen.blit(hscore,hscoreRect)


            # Get the score from the current game
##            current_score = score1
            # See if we have a new high score
            if current_score > high_score:
            # We do! Save to disk
    ##            print("Yea! New high score!")
                save_high_score(current_score)
    ##            counter = False
    ##        else:
    ##            print("Better luck next time.")
    ##            counter = False
            
    ##        print("message to screen executed")

        else:
            pygame.font.init()
            Replay("Congratulations ! You have beaten the game.",green,height/8)
            #this loop executes when exitcode=1 i.e time elapsed > 90 seconds
    ##        font = pygame.font.Font("font.ttf", 24)
            counter = True
            text = font.render("Accuracy: "+str(accuracy)+"% Score :"+str(current_score), True, green)
            textRect = text.get_rect()
            textRect.centerx = screen.get_rect().centerx
            textRect.centery = screen.get_rect().centery+24
            screen.blit(youwin, (0,0))
            screen.blit(text, textRect)


            high_score = get_high_score()
            hscore = font.render("All Time High Score: "+str(high_score), True, green)
            hscoreRect = hscore.get_rect()
            hscoreRect.centerx = screen.get_rect().centerx
            hscoreRect.centery = screen.get_rect().centery+60
            screen.blit(hscore,hscoreRect)

            
            # Get the score from the current game
            current_score = score1
            # See if we have a new high score
            if current_score > high_score:
            # We do! Save to disk
    ##            print("Yea! New high score!")
                save_high_score(current_score)
    ##            counter = False
    ##        else:
    ##            print("Better luck next time.")
    ##            counter = False
            
    ##        print("message to screen executed")
       
def Replay(msg,color,h):
    screen_text = font.render(msg, True , color)
    screen.blit(screen_text, [0,h])

def level_display_screen(level_number):
##    t2=clock.tick()
    t0 = time.time()
    boole = True
    screen.fill(rCBack)
    while boole == True:
        t1 = time.time()
        dt = t1 - t0
##        print level_number
##        print "sdfsdgvsdgvsdg  "+str(dt)
        if level_number == 0:
            Replay("                       Level 1",green,height/2)
        if level_number == 30:
            Replay("                       Level 1",green,height/2)
        if level_number == 10:
                   Replay("                        Level 2",green,height/2)
        if level_number == 20:
                   Replay("                        Level 3",green,height/2)
##        if level_number == 40:
##                   Replay("                        Level 3",green,height/2)

        if dt >= 1.5:
                          boole = False
                          t0 = t1
        pygame.display.update()
        Intro_clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
# 
# 4 - keep looping through
def gameloop(difficulty):
    # initialize the t0 variable, "starting the stopwatch"
    t0 = time.time()
    playerpos=[320,390] #variable to track position of player
    acc=[0,0] #accuracy calculator 0-total bullets fired 1-bullets hit
    arrows=[] #list of bullets
    badtimer=100
    badtimer1=0
    badguys=[[0,100]]
    healthvalue=200
    global level_counter
    global score1
##    Off_Screen_Enemy_Spaceship_Counter=0
##    Enemy_Spaceship_Arrow_Hit_Counter=0
##    Bullet_Pop_Off_Screen_Counter=0
##    Badrect_Colliderect_Playerrect_Counter=0
    snow_flakes_list = []
    loc_x, loc_y = 0, 0
##    num=0
    zz=1
##    score1=0
    clock=pygame.time.Clock()
    GameExit = False #before it was running = 1
    GameOver = False
    exitcode = 0
    counter = True
    t5 = 0
    bb = 0
    while not GameExit:
        # calculate the time since some reference point (here the Unix Epoch)
        t1 = time.time()
        if t5==0:
            dt=t1-t0
        if t5>0:
            t0+=t5
            dt=t1-t0
##            print t5
##            print dt
            t5 = 0
        badtimer-=1
##        clock.tick(FPS)
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
                    level_counter += 1
##                    print level_counter
                    if level_counter == 40:
                        level_counter = 10
                    zz=2
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
##                arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
                screen.blit(arrow, (projectile[1], projectile[2]))
        # 6.3 - Draw enemy space ships
        if badtimer==0:
            badguys.append([random.randint(22,605),0])
            badtimer=100-(badtimer1*2)
            if badtimer1>=35:
                badtimer1=35
            else:
                badtimer1+=5
##        print "afdfsdfsdf" ,badtimer
##        print "kjk" ,badtimer1
        index=0
        for badguy in badguys:
            if badguy[1]>480:
                badguys.pop(index)
##                Off_Screen_Enemy_Spaceship_Counter+=1
##                print "Enemy Spaceship pop from bottom screen"
##                print Off_Screen_Enemy_Spaceship_Counter
##            if (((index)%3)==0):
##                badguy [1]+= 7
##                badguy [0]+= 2
##            else:
##                badguy[1]+=3
##                badguy [0]-=2#speed of enemy space ships change 3 to others to hf

##            level(level_counter,badguy,index)
##            print "kajdnaksd", level_counter
            
            if level_counter == 10:
                badguy[1]+=3
            if level_counter == 20:
                if (((index)%3)==0):
                    badguy [1]+= 7
                else:
                    badguy[1]+=3

            if level_counter == 30:
                if (((index)%3)==0):
                    badguy [1]+= 7
                    badguy [0]+= 2
                else:
                    badguy[1]+=3
                    badguy [0]-=2



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
                healthvalue -=difficulty
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
                    if difficulty == 20:
                        score1+=1 #score increment...need to enhance it !
                    if difficulty == 40:
                        score1 += 2
                    if difficulty == 100:
                        score1 += 3
                    enemy.play()
                    acc[0]+=1
                    sprite(128, 120,badguy[0],badguy[1])
##                    print index
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
##            a= random.randint(1,4)
##            if a == 1:
##                screen.blit(badguyimg1,( badguy[0], badguy[1]))#unable to use different spaceships now.
                
##            if a == 2:
            screen.blit(badguyimg2, ( badguy[0], badguy[1]))#will try later :/
##                
##            if a == 3:
##                screen.blit(badguyimg3, ( badguy[0], badguy[1]))
##                
##            if a == 4:
##                screen.blit(badguyimg4,( badguy[0], badguy[1]))
##                
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

        position=pygame.mouse.get_pos()
        playerpos[0]=position[0] ##did for mouse movement of player but did not work :/
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
            if event.type==pygame.MOUSEBUTTONDOWN:
               keys[0] = True                
            if event.type == pygame.KEYDOWN:
##                if event.key==K_a:
##                    keys[0]=True
##                elif event.key==K_d:
##                    keys[1]=True
##                if event.key == K_w:
##                    pygame.display.set_mode((width, height))
##                if event.key == K_e:
##                    pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                if event.key == K_ESCAPE:
                    if screen.get_flags() & FULLSCREEN:
                        pygame.display.set_mode((width, height))
                if event.key == K_f:
                    if screen.get_flags() & FULLSCREEN:
                        pygame.display.set_mode((width, height))
                    else:
                        pygame.display.set_mode((width, height), pygame.FULLSCREEN)


                if event.key==K_p:
##                    pause()
                    t2=pause() #pause function called
                    t5 = int (t2/1000)
##                    if t5>0:
##                        print t5
##                        dt-=t5
##                        print dt
##            if event.type == pygame.KEYUP:
##                if event.key==pygame.K_a:
##                    keys[0]=False
##                elif event.key==pygame.K_d:
##                    keys[1]=False
            if event.type==pygame.MOUSEBUTTONUP:
                keys[0] = False
##            if event.type==pygame.MOUSEBUTTONDOWN:
##                shoot.play()
##                position=pygame.mouse.get_pos()
##                acc[1]+=1
##                arrows.append([math.atan2(position[1]-playerpos1[1],0),playerpos1[0]+60,playerpos1[1]+40])
##                print ([math.atan2(position[1]-(playerpos1[1]),position[0]-(playerpos1[0])),playerpos1[0]+60,playerpos1[1]+32]) 
##        if keys[0]:
##            playerpos[0]-=4
##        elif keys[1]:
##            playerpos[0]+=4
        if playerpos[0]>590: #check for right boundary
            playerpos[0]=590
        if playerpos[0]<0: #check for left boundary
            playerpos[0]=0
        if keys[0]:
            bb+=1
            if bb == (FPS/5): #60 FPS so it will fire 5 times in 1 second
                shoot.play()
##                position=pygame.mouse.get_pos()
                acc[1]+=1
                angle1 = math.atan2((position[1]-100)-playerpos1[1],0)
                if angle1 > 0:
                    angle1 *= -1
                if angle1 == 0:
                    angle1 = -1.57079632679
                arrows.append([angle1,playerpos1[0]+60,playerpos1[1]+40])
##                print angle1
                bb = 0
        clock.tick(FPS)
                

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
        score2 = score1

    while GameOver == True:
        screen.fill(rCBack)
        Message_to_Screen(exitcode,accuracy,score2,counter)
        h=height/1.75
        if exitcode==0:
            level_counter = 0
            score1=0
            button("Play Again",100,380,150,50,dark_green,green,action="Play")
            button("Quit",400,380,100,50,red,light_red,action = "Quit")

        else:
            if level_counter != 30:
    ##            if level_counter == 1:
    ##                level_counter = 2
    ##            if level_counter== 2:
    ##                level_counter=3
                
    ##            print level_counter
                button("Play Next Level",100,380,200,50,dark_green,green,action="Play")
                button("Quit",400,380,100,50,red,light_red,action = "Quit")
            else:
                score1=0
                button("Play Again",100,380,150,50,dark_green,green,action="Play")
                button("Credits",300,380,100,50,yellow,light_yellow,action = "Credits")
                button("Quit",450,380,100,50,red,light_red,action = "Quit")
                
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
##            if event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_q:
##                    GameExit= True
##                    GameOver= False
##                    pygame.quit()
##                    sys.exit()
##                if event.key == pygame.K_c:
##                    GameExit=False
##                    gameloop()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

intro_screen()
