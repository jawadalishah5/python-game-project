import pygame
import time
import random

pygame.init()

over_sound= pygame.mixer.Sound("over.wav")
pygame.mixer.music.load("chase.wav")


black=(0,0,0)
blue=(0,0,255)
green=(0,155,0)
red=(255,0,0)
white=(255,255,255)
magenta=(255,0,255)
yellow=(150,150,0)
bg=(0,255,200)

clock=pygame.time.Clock()
FPS=11
dis_wid,dis_high=720,600
gamedisplay=pygame.display.set_mode((dis_wid,dis_high))
pygame.display.set_caption("Dodge the Objects")

#CHARACTER IMAGE
char_img=pygame.image.load('character.png')
char_img=pygame.transform.scale(char_img,(60,60))    
def char(x,y):
    gamedisplay.blit(char_img,(x,y))

#APPLE IMAGE
apple_img=pygame.image.load('apple.png')
apple_img=pygame.transform.scale(apple_img,(60,60))
def apple(x,y):
    gamedisplay.blit(apple_img,(x,y))

#Hurdle IMAGE
hurdle_img=pygame.image.load('hurdles.png')
hurdle_img=pygame.transform.scale(hurdle_img,(60,60))
def hurdles(ballX, ballY):
    for i in ballX:
        gamedisplay.blit(hurdle_img,(i,ballY))

    
#DISPLAY THE MESSAGE IF ANY EVENT HAPPEN
def screen_msg(msg,color,X,Y,size):
    font=pygame.font.SysFont(None,size)
    screen_txt=font.render(msg,True,color)
    gamedisplay.blit(screen_txt,[X,Y])
        
    


def game_loop():
    gameExit=False
    gameOver=False

    life=50
    pygame.mixer.music.play(-1)
    color=green
    ball_startY=-300
    ball_speed=20
    score=0
    ball_width, ball_height=60,60
    move_x=dis_wid//2
    move_y=dis_high//2
    change_x,change_y=0,0
    multiple_score,i=1,1

    ball_startX=[]
    i=round(random.randint(0,dis_wid- ball_width))
    ball_startX.append(i)

    appleX=round(random.randint(0,dis_wid - ball_width)/60.0)*60.0
    appleY=round(random.randint(0, dis_high - ball_width)/60.0)*60.0

    
    #GAME LOOP
    while not gameExit: 
        
        #IF GAME IS OVER
        while gameOver :
            
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(over_sound)
            
            gamedisplay.fill(magenta)
            screen_msg("Your score is ",white,dis_wid//4,dis_high//4,30)
            screen_msg(str(score),green,dis_wid//2, dis_high//4,50)
            apple(dis_wid//4,dis_high//3)
            gamedisplay.blit(hurdle_img,((dis_wid//4)+70,dis_high//3))
            char((dis_wid//4)+140, dis_high//3)
            screen_msg("Game over! Press Y  to play press N to Quit",white,dis_wid//4,dis_high//2,30)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_n:
                        gameExit=True
                        gameOver=False
                    elif event.key==pygame.K_y:
                        game_loop()


        #EVENT LOOP
        for event in pygame.event.get():
            
            
            if event.type == pygame.QUIT:
                gameExit=True
           
            if event.type== pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    change_y=0
                    change_x= -ball_width
                elif event.key==pygame.K_RIGHT:
                    change_y=0
                    change_x=ball_width
                elif event.key==pygame.K_UP:
                    change_x=0
                    change_y= -ball_width
                elif event.key==pygame.K_DOWN:
                    change_x=0
                    change_y=ball_width

            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    change_x=0
                if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    change_y=0


        if move_x > dis_wid - ball_width:
            gameOver=True
        elif move_x < 0:
            gameOver=True
        if move_y > dis_high - ball_width:
            gameOver=True
        elif move_y<0:
            gameOver=True
        move_x+= change_x
        move_y+= change_y
        gamedisplay.fill(bg)



        #hurdles(ballX, ballY)
        hurdles(ball_startX, ball_startY)
        ball_startY += ball_speed
        
        char(move_x, move_y)
        screen_msg("SCORE: "+str(score),black,50,50,20)        
        screen_msg("HEALTH: ",black,540,54,20)
        pygame.draw.rect(gamedisplay,color,[600,50,life,20])
        
        apple(appleX,appleY)
        pygame.display.update()
        clock.tick(FPS)

        if move_x == appleX and move_y == appleY:
            score+=10
            appleX=round(random.randint(0,dis_wid - ball_width)/60.0)*60.0
            appleY=round(random.randint(0, dis_high - ball_height)/60.0)*60.0

        for i in ball_startX:
            if (move_x >= i and move_x<i+ball_width and move_y >= ball_startY and move_y<ball_startY+ball_width) or (move_x + ball_width > i and move_x +ball_width < i + ball_width and move_y >= ball_startY and move_y  < ball_startY+ball_height) or (move_x >= i and move_x< i + ball_width and move_y + ball_height>=ball_startY and move_y + ball_height<ball_startY+ball_height) or (move_x+ball_width > i and move_x + ball_width< i + ball_width and move_y + ball_height>=ball_startY and move_y + ball_height<ball_startY+ball_height) :
                life-=5
                if life<=25:
                    color=yellow
                if life<=15:
                    color=red
                if life<=0:
                    
                    gameOver=True

        if ball_startY >= dis_high:
            ball_startY=0
            if score < 30*multiple_score:
                ball_startX=[0]
            elif score >= 30*multiple_score and score < (30*multiple_score)+30:
                ball_startX=[0,0]
            elif score >=(30*multiple_score)+30 and score< (30*multiple_score)+60:
                ball_startX=[0,0,0]
            elif score >= (30*multiple_score)+60 and score< (30*multiple_score)+90:
                ball_startX=[0,0,0,0]

            elif score>=(30*multiple_score)+90:
                i+=1
                ball_speed+=20
                multiple_score +=4
                ball_startX=[0]
                
            
            for i in range(len(ball_startX)):
                ball_startX[i]=round(random.randint(0,dis_wid - ball_width))
                    




    pygame.quit()
    quit()

gamedisplay.fill(yellow)
screen_msg("Hello! Let's play the game called 'Dodge the Balls'",white,60,60,30)
screen_msg("(In this game, you have to collect as many green faces as you can",red,60,100,25)
screen_msg("and avoid those red hurdles Otherwise you will lose your lives)",red,60,130,25)
apple(60,200)
gamedisplay.blit(hurdle_img,(130,200))
char(200,200)


screen_msg("Let's Start :) Press P to play or Q to quit",white,60,400,30)

pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_p:
                game_loop()
            elif event.key==pygame.K_q:
                pygame.quit()
                quit()
            else:
                continue
            


