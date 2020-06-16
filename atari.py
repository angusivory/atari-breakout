#atari breakout 
import time
import random
import pygame
import math
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
blues = [(0,0,90), (0,0,145), (0,0,200), (0,0,255)]
reds = [(90,0,0), (145,0,0), (200,0,0), (255,0,0)]
oranges = [(90,58,0), (145,93,0), (200,129,0), (255,165,0)]
greens = [(0,90,0), (0,145,0), (0,200,0), (0,255,0)]
golds = [(90,78,0), (145,126,0), (200,174,0), (255,223,0)]
greys = [(90,90,90), (145,145,145), (200,200,200), (255,255,255)]
levelColours = [blues, reds, oranges, greens, golds, greys]
speed = 40
x1 = 350
y1 = 570
xchange = 0

#set up ball
ballx = 450
bally = 500
ballxchanges = [3,4,5,6,7,8,9,9,10]
ballychanges = [10,9,9,8,7,6,5,4,3]
num = random.randint(0, len(ballxchanges) -1)
ballxchange = ballxchanges[num]
ballychange = -ballychanges[num]
balldirection = ""

clock = pygame.time.Clock()
newLevel = True
game_over = False
score = 0
bounces = 0
lives = 3
level = 1
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
layers = [(layer1, layer1cumulative), (layer2, layer2cumulative), (layer3, layer3cumulative), (layer4, layer4cumulative)]
numberOfBlocksThatAreFalse = 0


#put text on the screen
font_style = pygame.font.SysFont(None, 50)
def message(msg, color, msgx, msgy):
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [msgx, msgy])

#put layers of randomly lengthed blocks on the screen for each new level
def popLevel(layer, layercumulative):
    blockx = 0
    while blockx < window_width - 210:
        
        length = round(random.randint(50, 180) / 10) * 10
        layer.append((length, True))
        blockx += length + 5
        layercumulative.append(blockx)

    #inneficient, but the only way (that i can think of currently): this is so that there are no 10-pixel blocks as the ball isn't able to hit them, 10px is not wide enough.
    blockwindowdiff = window_width - blockx
    if blockwindowdiff <= 40:
        layer.append((50, True))
        blockx += length + 5
        layercumulative.append(blockx)
    elif 40 < blockwindowdiff <= 100:
        layer.append((int(blockwindowdiff/2-10), True))
        blockx += int(blockwindowdiff/2-5)
        layercumulative.append(blockx)
        layer.append((int(blockwindowdiff/2+10), True))
        blockx += int(blockwindowdiff/2+5)
        layercumulative.append(blockx)
    elif 100 < blockwindowdiff <= 150:
        if random.randint(1,2) == 1:
            layer.append((blockwindowdiff, True))
            blockx += blockwindowdiff+5
            layercumulative.append(blockx)
        else:
            layer.append((int(blockwindowdiff/2-10), True))
            blockx += int(blockwindowdiff/2-5)
            layercumulative.append(blockx)
            layer.append((int(blockwindowdiff/2+10), True))
            blockx += int(blockwindowdiff/2+15)
            layercumulative.append(blockx)
    else:
        if random.randint(1,2) == 1:
            layer.append((int(blockwindowdiff/2-10), True))
            blockx += int(blockwindowdiff/2-5)
            layercumulative.append(blockx)
            layer.append((int(blockwindowdiff/2+10), True))
            blockx += int(blockwindowdiff/2+15)
            layercumulative.append(blockx)
        else:
            layer.append((int(blockwindowdiff/3-10), True))
            blockx += int(blockwindowdiff/3-5)
            layercumulative.append(blockx)
            layer.append((int(blockwindowdiff/3+10), True))
            blockx += int(blockwindowdiff/3+15)
            layercumulative.append(blockx)
            layer.append((int(blockwindowdiff/3+10), True))
            blockx += int(blockwindowdiff/3+15)
            layercumulative.append(blockx)






def drawBlocks(blockx, colourlist, l1, l2, l3, l4):
    for xl1, status in l1:
        if status == True:
            pygame.draw.rect(window, colourlist[0], [blockx, 70, xl1, 70])
        blockx += xl1 + 5
    blockx = 0
    for xl2, status in l2:
        if status == True:
            pygame.draw.rect(window, colourlist[1], [blockx, 145, xl2, 70])
        blockx += xl2 + 5
        
    blockx = 0
    for xl3, status in l3:
        if status == True:
            pygame.draw.rect(window, colourlist[2], [blockx, 220, xl3, 70])
        blockx += xl3 + 5
    blockx = 0
    for xl4, status in l4:
        if status == True:
            pygame.draw.rect(window, colourlist[3], [blockx, 295, xl4, 70])
        blockx += xl4 + 5
    blockx = 0

def ifblockhit(layer, layercumulative, ballychange, score):
    number = 0
    for item in layercumulative:
        if number == 0:
            if ballx < item:
                value, status = layer[number]
                layer[number] = (value, False)
                score += bounces
                if layer == layer4:
                    score += 1
                elif layer == layer3:
                    score += 2
                elif layer == layer2:
                    score += 3
                else:
                    score += 4

        else:
            if ballx < item and ballx >= layercumulative[number-1]:
                value, status = layer[number]
                layer[number] = (value, False)
                score += bounces
                if layer == layer4:
                    score += 1
                elif layer == layer3:
                    score += 2
                elif layer == layer2:
                    score += 3
                else:
                    score += 4
        number += 1
    #print(numberOfBlocksThatAreFalse)
    return score

def setUpLevel(level, l1, l2, l3, l4, l1c, l2c, l3c, l4c):
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    l1c = []
    l2c = []
    l3c = []
    l4c = []
    
    popLevel(l1, l1c)
    popLevel(l2, l2c)
    popLevel(l3, l3c)
    popLevel(l4, l4c)
    window.fill(black)
    #print("During level set up, layer1 =", l1)
    drawBlocks(blockx, levelColours[(level - 1)%len(levelColours)], l1, l2, l3, l4)
    #print("drawn blocks")
    message("Level {}".format(level), white, 420, 10)
    pygame.display.update()
    time.sleep(1)
    return l1, l2, l3, l4, l1c, l2c, l3c, l4c



#game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                newLevel = True
                level += 1
            if event.key == pygame.K_c:
                newLevel = True



    window.fill(black)
    
    mouse = pygame.mouse.get_pos()
    x1 = mouse[0] - 100

    if x1 <= 0:
        x1 = 0
    elif x1 >= window_width - 200:
        x1 = window_width - 200

    drawBlocks(blockx, levelColours[(level - 1)%len(levelColours)], layer1, layer2, layer3, layer4)

    if newLevel == True:
        layer1, layer2, layer3, layer4, layer1cumulative, layer2cumulative, layer3cumulative, layer4cumulative = setUpLevel(level, layer1, layer2, layer3, layer4, layer1cumulative, layer2cumulative, layer3cumulative, layer4cumulative)
        blockx = 0
        newLevel = False
        numberOfBlocksThatAreFalse = 0
        lives = 3
        ballx = 450
        bally = 500
        num = random.randint(0, len(ballxchanges) -1)
        ballxchange = -ballxchanges[num]
        ballychange = -ballychanges[num]



    #ball movement
    ballx += ballxchange
    bally += ballychange

    if ballx <= 10 or ballx >= window_width-10:
        ballxchange = -ballxchange
    if bally <= 10:
        ballychange = -ballychange
    
    #lose a life
    if bally >= window_height + 20:
        print("lost a life")
        time.sleep(1)
        ballx = 450
        bally = 500
        num = random.randint(0, len(ballxchanges) -1)
        ballxchange = -ballxchanges[num]
        ballychange = -ballychanges[num]
        lives -= 1
        if lives == 0:
            window.fill(black)
            message("GAME OVER", white, 50, 50)
            message("You scored {}".format(str(score)), white, 50, 110)
            pygame.display.update()
            time.sleep(2)
            game_over = True


    if ballychange > 0:
        balldirection = "down"
    else:
        balldirection = "up"


    if 560 <= bally <= 570 and balldirection == "down":
        bounces = 0
        if ballx >= x1 and ballx <= x1 + 200:
            xdiff = ballx - x1
            xdiff = int(xdiff/20)
            if ballxchange < 0:     #if ball direction is left
                if xdiff == 10:
                    ballychange = random.randint(-2,-1)
                    ballxchange = 10
                elif xdiff == 9:
                    ballychange = -4
                    ballxchange = 10
                elif xdiff == 8:
                    ballychange = -5
                    ballxchange = random.randint(8,9)
                elif xdiff == 7:
                    ballychange = -6
                    ballxchange = random.randint(7,9)
                elif xdiff == 6:
                    ballychange = -7
                    ballxchange = random.randint(6,8)
                elif xdiff == 5:
                    ballychange = -9
                    ballxchange = random.randint(-5,-3)
                elif xdiff == 4:
                    ballychange = -7
                    ballxchange = random.randint(-8,-6)
                elif xdiff == 3:
                    ballychange = -6
                    ballxchange = random.randint(-9,-7)
                else:
                    ballychange = -4
                    ballxchange = -9
                #ballxchange = xdiff - 1
                #ballychange = -(int(math.sqrt(10**2 - xdiff**2)))

            elif ballxchange > 0:   #if ball direction is right
                if xdiff == 1:
                    ballychange = random.randint(-2,-1)
                    ballxchange = -10
                elif xdiff == 2:
                    ballychange = -4
                    ballxchange = -10
                elif xdiff == 3:
                    ballychange = -5
                    ballxchange = random.randint(-9,-8)
                elif xdiff == 4:
                    ballychange = -6
                    ballxchange = random.randint(-9,-8)
                elif xdiff == 5:
                    ballychange = -7
                    ballchange = random.randint(-8,-6)
                elif xdiff == 6:
                    ballychange = -9
                    ballxchange = random.randint(3,5)
                elif xdiff == 7:
                    ballychange = -7
                    ballxchange = random.randint(6,8)
                elif xdiff == 8:
                    ballychange = -6
                    ballxchange = random.randint(7,9)
                else:
                    ballychange = -4
                    ballxchange = 9


    #if ball has hit a block
    if bally - 10 <= 365 and bally - 10 >= 350:
        if window.get_at((ballx, bally - 10)) in levelColours[(level - 1)%len(levelColours)]:
            if balldirection == "up":
                score = ifblockhit(layer4, layer4cumulative, ballychange, score)
            ballychange = -ballychange
            numberOfBlocksThatAreFalse += 1
    elif bally - 10 <= 290 and bally - 10 >= 275:
        if window.get_at((ballx, bally - 10)) in levelColours[(level - 1)%len(levelColours)] or window.get_at((ballx, bally + 10)) in levelColours[(level - 1)%len(levelColours)]:
            if balldirection == "up":
                score = ifblockhit(layer3, layer3cumulative, ballychange, score)
            else:
                score = ifblockhit(layer4, layer4cumulative, ballychange, score)
            ballychange = -ballychange
            numberOfBlocksThatAreFalse += 1
    elif bally - 10 <= 220 and bally - 10 >= 205:
        if window.get_at((ballx, bally - 10)) in levelColours[(level - 1)%len(levelColours)] or window.get_at((ballx, bally + 10)) in levelColours[(level - 1)%len(levelColours)]:
            if balldirection == "up":
                score = ifblockhit(layer2, layer2cumulative, ballychange, score)
            else:
                score = ifblockhit(layer3, layer3cumulative, ballychange, score)
            ballychange = -ballychange
            numberOfBlocksThatAreFalse += 1
    elif bally - 10 <= 145 and bally - 10 >= 130:
        if window.get_at((ballx, bally - 10)) in levelColours[(level - 1)%len(levelColours)] or window.get_at((ballx, bally + 10)) in levelColours[(level - 1)%len(levelColours)]:
            if balldirection == "up":
                score = ifblockhit(layer1, layer1cumulative, ballychange, score)
            else:
                score = ifblockhit(layer2, layer2cumulative, ballychange, score)
            ballychange = -ballychange
            numberOfBlocksThatAreFalse += 1
    elif bally - 10 <= 70 and bally - 10 >= 55:
        if window.get_at((ballx, bally + 10)) in levelColours[(level - 1)%len(levelColours)]:
            if balldirection == "down":
                score = ifblockhit(layer1, layer1cumulative, ballychange, score)
            ballychange = -ballychange
            numberOfBlocksThatAreFalse += 1


    if bally >= 295 and bally <= 365:
        for x in range(0, len(layer4cumulative)):
            if layer4cumulative[x] - 5 <= ballx <= layer4cumulative[x] + 5:
                if ballxchange < 0:
                    value, status = layer4[x]
                    if status == True:
                        layer4[x] = (value, False)
                        ballxchange = -ballxchange
                        score += bounces + 1
                        bounces += 1
                        numberOfBlocksThatAreFalse += 1
                else:
                    value, status = layer4[x+1]
                    if status == True:
                        layer4[x+1] = (value, False)
                        ballxchange = -ballxchange
                        score += bounces + 1
                        bounces += 1
                        numberOfBlocksThatAreFalse += 1

    elif bally >= 220 and bally <= 290:
        for x in range(0, len(layer3cumulative)):
            if layer3cumulative[x] - 5 <= ballx <= layer3cumulative[x] + 5:
                if ballxchange < 0:
                    value, status = layer3[x]
                    if status == True:
                        layer3[x] = (value, False)
                        ballxchange = -ballxchange
                        score += bounces + 2
                        bounces += 1
                        numberOfBlocksThatAreFalse += 1
                else:
                    value, status = layer3[x+1]
                    if status == True:
                        layer3[x+1] = (value, False)
                        ballxchange = -ballxchange
                        score += bounces +2
                        bounces += 1
                        numberOfBlocksThatAreFalse += 1

    elif bally >= 145 and bally <= 215:
        for x in range(0, len(layer2cumulative)):
            if layer2cumulative[x] - 5 <= ballx <= layer2cumulative[x] + 5:
                if ballxchange < 0:
                    value, status = layer2[x]
                    if status == True:
                        layer2[x] = (value, False)
                        ballxchange = -ballxchange
                        score += bounces + 3
                        bounces += 1
                        numberOfBlocksThatAreFalse += 1
                else:
                    value, status = layer2[x+1]
                    if status == True:
                        layer2[x+1] = (value, False)
                        ballxchange = -ballxchange
                        score += bounces + 3
                        bounces += 1
                        numberOfBlocksThatAreFalse += 1

    elif bally >= 70 and bally <= 140:
        for x in range(0, len(layer1cumulative)):
            if layer1cumulative[x] - 5 <= ballx <= layer1cumulative[x] + 5:
                if ballxchange < 0:
                    value, status = layer1[x]
                    if status == True:
                        layer1[x] = (value, False)
                        ballxchange = -ballxchange
                        score += bounces + 4
                        bounces += 1
                        numberOfBlocksThatAreFalse += 1
                else:
                    value, status = layer1[x+1]
                    if status == True:
                        layer1[x+1] = (value, False)
                        ballxchange = -ballxchange
                        score += bounces + 4
                        bounces += 1
                        numberOfBlocksThatAreFalse += 1

    #check if new level is required
    if numberOfBlocksThatAreFalse == len(layer1) + len(layer2) + len(layer3) + len(layer4):
        newLevel = True
        level += 1

    message(str(score), white, 0, 0)
    message("Level {}".format(level), white, 420, 10)
    if lives == 1:
        message(str(lives), red, 880, 0)
    else:
        message(str(lives), white, 880, 0)
    pygame.draw.circle(window, orange, (ballx, bally), 10)
    pygame.draw.rect(window, yellow, [x1, y1, 200, 15])
    pygame.display.update()
    clock.tick(speed)


pygame.quit()
quit()