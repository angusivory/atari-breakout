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
class Ball():

    def __init__(self, ballx, bally, balldirection, ballxchange, ballychange):
        self.ballx = ballx
        self.bally = bally
        self.ballxchange = ballxchange
        self.ballychange = ballychange
        self.balldirection = balldirection

    def __str__(self):
        return f"The ball is located at ({self.ballx},{self.bally}), direction: {self.balldirection}."

ballxchanges = [3,4,5,6,7,8,9,9,10]
ballychanges = [10,9,9,8,7,6,5,4,3]
num = random.randint(0, len(ballxchanges) - 1)
atariBall = Ball(450, 500, "", ballxchanges[num], ballychanges[num])


clock = pygame.time.Clock()
newLevel = True
game_over = False
score = 0
bounces = 0
lives = 3
level = 1
#layers = [(layer1, layer1cumulative), (layer2, layer2cumulative), (layer3, layer3cumulative), (layer4, layer4cumulative)]
numberOfBlocksThatAreFalse = 0

class Wall():
    def __init__(self, layer1, layer2, layer3, layer4, layer1cumulative, layer2cumulative, layer3cumulative, layer4cumulative, blockx, length):
        self.layer1 = layer1
        self.layer2 = layer2
        self.layer3 = layer3
        self.layer4 = layer4
        self.layer1cumulative = layer1cumulative
        self.layer2cumulative = layer2cumulative
        self.layer3cumulative = layer3cumulative
        self.layer4cumulative = layer4cumulative
        self.blockx = blockx
        self.length = length

    def __str__(self):
        return f"layer1: {self.layer1}, layer2: {self.layer2}, layer3: {self.layer3}, layer4: {self.layer4}"

    def clearLayers(self):
        self.layer1 = []
        self.layer2 = []
        self.layer3 = []
        self.layer4 = []
        self.layer1cumulative = []
        self.layer2cumulative = []
        self.layer3cumulative = []
        self.layer4cumulative = []

    def drawBlocks(self, theWall, colourlist):
        for xl1, status in theWall.layer1:
            if status == True:
                pygame.draw.rect(window, colourlist[0], [theWall.blockx, 70, xl1, 70])
            theWall.blockx += xl1 + 5
        theWall.blockx = 0
        for xl2, status in theWall.layer2:
            if status == True:
                pygame.draw.rect(window, colourlist[1], [theWall.blockx, 145, xl2, 70])
            theWall.blockx += xl2 + 5
            
        theWall.blockx = 0
        for xl3, status in theWall.layer3:
            if status == True:
                pygame.draw.rect(window, colourlist[2], [theWall.blockx, 220, xl3, 70])
            theWall.blockx += xl3 + 5
        theWall.blockx = 0
        for xl4, status in theWall.layer4:
            if status == True:
                pygame.draw.rect(window, colourlist[3], [theWall.blockx, 295, xl4, 70])
            theWall.blockx += xl4 + 5
        theWall.blockx = 0

theWall = Wall([], [], [], [], [], [], [], [], 0, 0, )



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








def ifblockhit(layer, layercumulative, ball, score, theWall):
    number = 0
    for item in layercumulative:
        if number == 0:
            if atariBall.ballx < item:
                value, status = layer[number]
                layer[number] = (value, False)
                score += bounces
                if layer == theWall.layer4:
                    score += 1
                elif layer == theWall.layer3:
                    score += 2
                elif layer == theWall.layer2:
                    score += 3
                else:
                    score += 4

        else:
            if atariBall.ballx < item and atariBall.ballx >= layercumulative[number-1]:
                value, status = layer[number]
                layer[number] = (value, False)
                score += bounces
                if layer == theWall.layer4:
                    score += 1
                elif layer == theWall.layer3:
                    score += 2
                elif layer == theWall.layer2:
                    score += 3
                else:
                    score += 4
        number += 1
    #print(numberOfBlocksThatAreFalse)
    return score

def setUpLevel(level, theWall):
    theWall.clearLayers()
    
    popLevel(theWall.layer1, theWall.layer1cumulative)
    popLevel(theWall.layer2, theWall.layer2cumulative)
    popLevel(theWall.layer3, theWall.layer3cumulative)
    popLevel(theWall.layer4, theWall.layer4cumulative)
    window.fill(black)
    #print("During level set up, layer1 =", l1)
    theWall.drawBlocks(theWall, levelColours[(level - 1)%len(levelColours)])
    #print("drawn blocks")
    message("Level {}".format(level), white, 420, 10)
    pygame.display.update()
    time.sleep(1)
    return theWall



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
    ballhitblockquestionmark = False
    
    mouse = pygame.mouse.get_pos()
    x1 = mouse[0] - 100

    if x1 <= 0:
        x1 = 0
    elif x1 >= window_width - 200:
        x1 = window_width - 200

    theWall.drawBlocks(theWall, levelColours[(level - 1)%len(levelColours)])

    if newLevel == True:
        theWall = setUpLevel(level, theWall)
        theWall.blockx = 0
        newLevel = False
        numberOfBlocksThatAreFalse = 0
        lives = 3
        atariBall.ballx = 450
        atariBall.bally = 500
        num = random.randint(0, len(ballxchanges) -1)
        atariBall.ballxchange = -ballxchanges[num]
        atariBall.ballychange = -ballychanges[num]



    #ball movement
    atariBall.ballx += atariBall.ballxchange
    atariBall.bally += atariBall.ballychange

    if atariBall.ballx <= 10 or atariBall.ballx >= window_width-10:
        atariBall.ballxchange = -atariBall.ballxchange
    if atariBall.bally <= 10:
        atariBall.ballychange = -atariBall.ballychange
    
    #lose a life
    if atariBall.bally >= window_height + 20:
        print("lost a life")
        time.sleep(1)
        atariBall.ballx = 450
        atariBall.bally = 500
        num = random.randint(0, len(ballxchanges) -1)
        atariBall.ballxchange = -ballxchanges[num]
        atariBall.ballychange = -ballychanges[num]
        lives -= 1
        if lives == 0:
            window.fill(black)
            message("GAME OVER", white, 50, 50)
            message("You scored {}".format(str(score)), white, 50, 110)
            pygame.display.update()
            time.sleep(2)
            game_over = True


    if atariBall.ballychange > 0:
       atariBall. balldirection = "down"
    else:
        atariBall.balldirection = "up"


    if 560 <= atariBall.bally <= 570 and atariBall.balldirection == "down":
        bounces = 0
        if atariBall.ballx >= x1 and atariBall.ballx <= x1 + 200:
            xdiff = atariBall.ballx - x1
            xdiff = int(xdiff/20)
            if atariBall.ballxchange < 0:     #if ball direction is left
                if xdiff == 10:
                    atariBall.ballychange = random.randint(-2,-1)
                    atariBall.ballxchange = 10
                elif xdiff == 9:
                    atariBall.ballychange = -4
                    atariBall.ballxchange = 10
                elif xdiff == 8:
                    atariBall.ballychange = -5
                    atariBall.ballxchange = random.randint(8,9)
                elif xdiff == 7:
                    atariBall.ballychange = -6
                    atariBall.ballxchange = random.randint(7,9)
                elif xdiff == 6:
                    atariBall.ballychange = -7
                    atariBall.ballxchange = random.randint(6,8)
                elif xdiff == 5:
                    atariBall.ballychange = -9
                    atariBall.ballxchange = random.randint(-5,-3)
                elif xdiff == 4:
                    atariBall.ballychange = -7
                    atariBall.ballxchange = random.randint(-8,-6)
                elif xdiff == 3:
                    atariBall.ballychange = -6
                    atariBall.ballxchange = random.randint(-9,-7)
                else:
                    atariBall.ballychange = -4
                    atariBall.ballxchange = -9
                #ballxchange = xdiff - 1
                #ballychange = -(int(math.sqrt(10**2 - xdiff**2)))

            elif atariBall.ballxchange > 0:   #if ball direction is right
                if xdiff == 1:
                    atariBall.ballychange = random.randint(-2,-1)
                    atariBall.ballxchange = -10
                elif xdiff == 2:
                    atariBall.ballychange = -4
                    atariBall.ballxchange = -10
                elif xdiff == 3:
                    atariBall.ballychange = -5
                    atariBall.ballxchange = random.randint(-9,-8)
                elif xdiff == 4:
                    atariBall.ballychange = -6
                    atariBall.ballxchange = random.randint(-9,-8)
                elif xdiff == 5:
                    atariBall.ballychange = -7
                    atariBall.ballchange = random.randint(-8,-6)
                elif xdiff == 6:
                    atariBall.ballychange = -9
                    atariBall.ballxchange = random.randint(3,5)
                elif xdiff == 7:
                    atariBall.ballychange = -7
                    atariBall.ballxchange = random.randint(6,8)
                elif xdiff == 8:
                    atariBall.ballychange = -6
                    atariBall.ballxchange = random.randint(7,9)
                else:
                    atariBall.ballychange = -4
                    atariBall.ballxchange = 9



    #if ball has hit a block
    if atariBall.bally - 10 <= 365 and atariBall.bally - 10 >= 350:
        if window.get_at((atariBall.ballx, atariBall.bally - 10)) in levelColours[(level - 1)%len(levelColours)]:
            if atariBall.balldirection == "up":
                score = ifblockhit(theWall.layer4, theWall.layer4cumulative, atariBall.ballychange, score, theWall)
            atariBall.ballychange = -atariBall.ballychange
            numberOfBlocksThatAreFalse += 1
            ballhitblockquestionmark = True
    elif atariBall.bally - 10 <= 290 and atariBall.bally - 10 >= 275:
        if window.get_at((atariBall.ballx, atariBall.bally - 10)) in levelColours[(level - 1)%len(levelColours)] or window.get_at((atariBall.ballx, atariBall.bally + 10)) in levelColours[(level - 1)%len(levelColours)]:
            if atariBall.balldirection == "up":
                score = ifblockhit(theWall.layer3, theWall.layer3cumulative, atariBall.ballychange, score, theWall)
            else:
                score = ifblockhit(theWall.layer4, theWall.layer4cumulative, atariBall.ballychange, score, theWall)
            atariBall.ballychange = -atariBall.ballychange
            numberOfBlocksThatAreFalse += 1
            ballhitblockquestionmark = True
    elif atariBall.bally - 10 <= 220 and atariBall.bally - 10 >= 205:
        if window.get_at((atariBall.ballx, atariBall.bally - 10)) in levelColours[(level - 1)%len(levelColours)] or window.get_at((atariBall.ballx, atariBall.bally + 10)) in levelColours[(level - 1)%len(levelColours)]:
            if atariBall.balldirection == "up":
                score = ifblockhit(theWall.layer2, theWall.layer2cumulative, atariBall.ballychange, score, theWall)
            else:
                score = ifblockhit(theWall.layer3, theWall.layer3cumulative, atariBall.ballychange, score, theWall)
            atariBall.ballychange = -atariBall.ballychange
            numberOfBlocksThatAreFalse += 1
            ballhitblockquestionmark = True
    elif atariBall.bally - 10 <= 145 and atariBall.bally - 10 >= 130:
        if window.get_at((atariBall.ballx, atariBall.bally - 10)) in levelColours[(level - 1)%len(levelColours)] or window.get_at((atariBall.ballx, atariBall.bally + 10)) in levelColours[(level - 1)%len(levelColours)]:
            if atariBall.balldirection == "up":
                score = ifblockhit(theWall.layer1, theWall.layer1cumulative, atariBall.ballychange, score, theWall)
            else:
                score = ifblockhit(theWall.layer2, theWall.layer2cumulative, atariBall.ballychange, score, theWall)
            atariBall.ballychange = -atariBall.ballychange
            numberOfBlocksThatAreFalse += 1
            ballhitblockquestionmark = True
    elif atariBall.bally - 10 <= 70 and atariBall.bally - 10 >= 55:
        if window.get_at((atariBall.ballx, atariBall.bally + 10)) in levelColours[(level - 1)%len(levelColours)]:
            if atariBall.balldirection == "down":
                score = ifblockhit(theWall.layer1, theWall.layer1cumulative, atariBall.ballychange, score, theWall)
            atariBall.ballychange = -atariBall.ballychange
            numberOfBlocksThatAreFalse += 1
            ballhitblockquestionmark = True

    if ballhitblockquestionmark == False:
        if atariBall.bally >= 295 and atariBall.bally <= 365:
            for x in range(0, len(theWall.layer4cumulative)):
                if theWall.layer4cumulative[x] - 5 <= atariBall.ballx <= theWall.layer4cumulative[x] + 5:
                    if atariBall.ballxchange < 0:
                        value, status = theWall.layer4[x]
                        if status == True:
                            theWall.layer4[x] = (value, False)
                            atariBall.ballxchange = -atariBall.ballxchange
                            score += bounces + 1
                            bounces += 1
                            numberOfBlocksThatAreFalse += 1
                    else:
                        value, status = theWall.layer4[x+1]
                        if status == True:
                            theWall.layer4[x+1] = (value, False)
                            atariBall.ballxchange = -atariBall.ballxchange
                            score += bounces + 1
                            bounces += 1
                            numberOfBlocksThatAreFalse += 1

        elif atariBall.bally >= 220 and atariBall.bally <= 290:
            for x in range(0, len(theWall.layer3cumulative)):
                if theWall.layer3cumulative[x] - 5 <= atariBall.ballx <= theWall.layer3cumulative[x] + 5:
                    if atariBall.ballxchange < 0:
                        value, status = theWall.layer3[x]
                        if status == True:
                            theWall.layer3[x] = (value, False)
                            atariBall.ballxchange = -atariBall.ballxchange
                            score += bounces + 2
                            bounces += 1
                            numberOfBlocksThatAreFalse += 1
                    else:
                        value, status = theWall.layer3[x+1]
                        if status == True:
                            theWall.layer3[x+1] = (value, False)
                            atariBall.ballxchange = -atariBall.ballxchange
                            score += bounces +2
                            bounces += 1
                            numberOfBlocksThatAreFalse += 1

        elif atariBall.bally >= 145 and atariBall.bally <= 215:
            for x in range(0, len(theWall.layer2cumulative)):
                if theWall.layer2cumulative[x] - 5 <= atariBall.ballx <= theWall.layer2cumulative[x] + 5:
                    if atariBall.ballxchange < 0:
                        value, status = theWall.layer2[x]
                        if status == True:
                            theWall.layer2[x] = (value, False)
                            atariBall.ballxchange = -atariBall.ballxchange
                            score += bounces + 3
                            bounces += 1
                            numberOfBlocksThatAreFalse += 1
                    else:
                        value, status = theWall.layer2[x+1]
                        if status == True:
                            theWall.layer2[x+1] = (value, False)
                            atariBall.ballxchange = -atariBall.ballxchange
                            score += bounces + 3
                            bounces += 1
                            numberOfBlocksThatAreFalse += 1

        elif atariBall.bally >= 70 and atariBall.bally <= 140:
            for x in range(0, len(theWall.layer1cumulative)):
                if theWall.layer1cumulative[x] - 5 <= atariBall.ballx <= theWall.layer1cumulative[x] + 5:
                    if atariBall.ballxchange < 0:
                        value, status = theWall.layer1[x]
                        if status == True:
                            theWall.layer1[x] = (value, False)
                            atariBall.ballxchange = -atariBall.ballxchange
                            score += bounces + 4
                            bounces += 1
                            numberOfBlocksThatAreFalse += 1
                    else:
                        value, status = theWall.layer1[x+1]
                        if status == True:
                            theWall.layer1[x+1] = (value, False)
                            atariBall.ballxchange = -atariBall.ballxchange
                            score += bounces + 4
                            bounces += 1
                            numberOfBlocksThatAreFalse += 1

    #check if new level is required
    if numberOfBlocksThatAreFalse == len(theWall.layer1) + len(theWall.layer2) + len(theWall.layer3) + len(theWall.layer4):
        newLevel = True
        level += 1

    message(str(score), white, 0, 0)
    message("Level {}".format(level), white, 420, 10)
    if lives == 1:
        message(str(lives), red, 880, 0)
    else:
        message(str(lives), white, 880, 0)
    pygame.draw.circle(window, orange, (atariBall.ballx, atariBall.bally), 10)
    pygame.draw.rect(window, yellow, [x1, y1, 200, 15])
    pygame.display.update()
    clock.tick(speed)


pygame.quit()
quit()