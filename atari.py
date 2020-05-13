#atari breakout 
import time
import random
import pygame
pygame.init()

#set up window
window_width = 900
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Atari Breakout')


#define constant variables
red = (255,0,0)
orange = (235, 134, 52)
yellow = (220, 255, 10)
lime = (171, 235, 52)
green = (0,255,0)
darkgreen = (28, 128, 51)
blue = (0,0,255)
purple = (171, 52, 235)
white = (255, 255, 255)
black = (0,0,0)
gold = (255, 223, 0)    #212, 175, 55
silver = (192, 192, 192)

speed = 40
x1 = 350
y1 = 570
xchange = 0

ballx = 450
bally = 500
ballxchange = random.randint(1, 10)
ballychange = random.randint(-10, -1)
balldirection = ""

clock = pygame.time.Clock()
newLevel = True
game_over = False
score = 0
length = 0
blockx = 0
layer1 = []
layer2 = []
layer3 = []
layer4 = []
layer1cumulative = []
layer2cumulative = []
layer3cumulative = []
layer4cumulative = []

class Ball:
    def __init__(self):
        self.ballx = 450
        self.bally = 500
        self.ballxchange = random.randint(1, 10)
        self.ballychange = random.randint(-10, -1)

    def print(self):
        print('In class method: ballx is {}'.format(self.ballx))

def ball_print(ball):
    print('Function Ball x {}, y {}'.format(ball.ballx, ball.bally))

#put text on the screen
font_style = pygame.font.SysFont(None, 50)
def message(msg, color, msgx, msgy):
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [msgx, msgy])

#put layers of randomly lengthed blocks on the screen for each new level
def popLevel(layer, layercumulative):
    blockx = 0
    while blockx < window_width:
        
        length = round(random.randint(50, 200) / 10) * 10
        layer.append((length, True))
        blockx += length + 5
        layercumulative.append(blockx)

def printLayer(layer, layercumulative):
    print(layer)
    print(layercumulative)

def printLayers():
    print(layer1)
    print(layer1cumulative)
    print(layer2)
    print(layer2cumulative)
    print(layer3)
    print(layer3cumulative)
    print(layer4)
    print(layer4cumulative)

def levelBlocks():
    popLevel(layer1, layer1cumulative)
    popLevel(layer2, layer2cumulative)
    popLevel(layer3, layer3cumulative)
    popLevel(layer4, layer4cumulative)

def ifblockhit(layer, layercumulative):
    number = 0
    for item in layercumulative:
        if number == 0:
            if ballx < item:
                value, status = layer[number]
                layer[number] = (value, False)

        else:
            if ballx < item and ballx >= layercumulative[number-1]:
                value, status = layer[number]
                layer[number] = (value, False)
        number += 1

#my_ball = Ball()
#ball_print(my_ball)
#my_ball.print()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xchange = -10
            elif event.key == pygame.K_RIGHT:
                xchange = 10
            elif event.key == pygame.K_DOWN:
                xchange = 0

            if event.key == pygame.K_w:
                bally -= 10
            elif event.key == pygame.K_s:
                bally += 10
            elif event.key == pygame.K_a:
                ballx -= 10
            elif event.key == pygame.K_d:
                ballx += 10


    window.fill(black)
    x1 += xchange

    if x1 <= 0:
        x1 = 0
    elif x1 >= window_width - 200:
        x1 = window_width - 200

    if newLevel == True:
        newLevel = False
        levelBlocks()
        blockx = 0

    for xl1, status in layer1:                                          #maybe functionize this like popLevel() on line 57
        if status == True:
            pygame.draw.rect(window, (0, 0, 90), [blockx, 70, xl1, 70])
        blockx += xl1 + 5
    blockx = 0
    for xl2, status in layer2:
        if status == True:
            pygame.draw.rect(window, (0, 0, 145), [blockx, 145, xl2, 70])
        blockx += xl2 + 5
        
    blockx = 0
    for xl3, status in layer3:
        if status == True:
            pygame.draw.rect(window, (0, 0, 200), [blockx, 220, xl3, 70])
        blockx += xl3 + 5
    blockx = 0
    for xl4, status in layer4:
        if status == True:
            pygame.draw.rect(window, blue, [blockx, 295, xl4, 70])
        blockx += xl4 + 5
    blockx = 0


    #ball movement
    ballx += ballxchange
    bally += ballychange

    if ballx <= 0 or ballx >= window_width-10:
        ballxchange = -ballxchange
    if bally <= 10:
        ballychange = -ballychange
    if bally >= 560:
        if ballx >= x1 and ballx <= x1 + 200:
            ballychange = -ballychange
        else:
            print("lost a life")

    if ballychange > 0:
        balldirection = "down"
    else:
        balldirection = "up"


    #if ball has hit a block
    if bally - 10 <= 365 and bally - 10 >= 350:
        if balldirection == "up":
            ifblockhit(layer4, layer4cumulative)
        ballychange = -ballychange
    elif bally - 10 <= 290 and bally - 10 >= 275:
        if balldirection == "up":
            ifblockhit(layer3, layer3cumulative)
        else:
            ifblockhit(layer4, layer4cumulative)
        ballychange = -ballychange
    elif bally - 10 <= 220 and bally - 10 >= 205:
        if balldirection == "up":
            ifblockhit(layer2, layer2cumulative)
        else:
            ifblockhit(layer3, layer3cumulative)
        ballychange = -ballychange
    elif bally - 10 <= 145 and bally - 10 >= 130:
        if balldirection == "up":
            ifblockhit(layer1, layer1cumulative)
        else:
            ifblockhit(layer2, layer2cumulative)
        ballychange = -ballychange
    elif bally - 10 <= 70 and bally - 10 >= 55:
        if balldirection == "down":
            ifblockhit(layer1, layer1cumulative)
        ballychange = -ballychange


    pygame.draw.circle(window, orange, (ballx, bally), 10)
    pygame.draw.rect(window, yellow, [x1, y1, 200, 15])
    pygame.display.update()
    clock.tick(speed)


pygame.quit()
quit()