#atari breakout 
import time
import random
import pygame
pygame.init()

#set up window
window_width = 900
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Block breaker')


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
clock = pygame.time.Clock()
newLevel = True
game_over = False
score = 0
length = 0
layer1 = []
layer2 = []
layer3 = []
layer4 = []
blockx = 0


#put text on the screen
font_style = pygame.font.SysFont(None, 50)
def message(msg, color, msgx, msgy):
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [msgx, msgy])

#put layers of randomly lengthed blocks on the screen for each new level
def levelBlocks(blockx):
    while blockx < window_width:
        length = round(random.randint(50, 200) / 10) * 10
        layer1.append(length)
        blockx += length + 5
    blockx = 0
    while blockx < window_width:
        length = round(random.randint(50, 200) / 10) * 10
        layer2.append(length)
        blockx += length + 5
    blockx = 0
    while blockx < window_width:
        length = round(random.randint(50, 200) / 10) * 10
        layer3.append(length)
        blockx += length + 5
    blockx = 0
    while blockx < window_width:
        length = round(random.randint(50, 200) / 10) * 10
        layer4.append(length)
        blockx += length + 5
    blockx = 0
    print(layer1)
    print(layer2)
    print(layer3)


#to calculate angle to bounce off blocks at, calculate gradient (y2-y1/x2-x1) and then do negative gradient of it


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

    window.fill(black)
    x1 += xchange

    if x1 <= 0:
        x1 = 0
    elif x1 >= window_width - 200:
        x1 = window_width - 200

    if newLevel == True:
        newLevel = False
        levelBlocks(blockx)
        blockx = 0

    for xl1 in layer1:
        pygame.draw.rect(window, (0, 0, 90), [blockx, 70, xl1, 70])
        blockx += xl1 + 5
    blockx = 0
    for xl2 in layer2:
        pygame.draw.rect(window, (0, 0, 145), [blockx, 145, xl2, 70])
        blockx += xl2 + 5
    blockx = 0
    for xl3 in layer3:
        pygame.draw.rect(window, (0, 0, 200), [blockx, 220, xl3, 70])
        blockx += xl3 + 5
    blockx = 0
    for xl4 in layer4:
        pygame.draw.rect(window, blue, [blockx, 295, xl4, 70])
        blockx += xl4 + 5
    blockx = 0

    pygame.draw.rect(window, yellow, [x1, y1, 200, 15])
    pygame.display.update()
    clock.tick(speed)


pygame.quit()
quit()