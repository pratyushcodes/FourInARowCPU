import pygame
import numpy as np
import time
import sys
from pygame.locals import  *
import multiplayerV4 as mp
import CPUEasyV4 as ce
import CPUMediumV4 as cm
import CPUHardV4 as ch

pygame.init() # initialize or start pygame

def bgMusic():
    from pygame import  mixer
    bgMusic = 'mixkit-natural-ambience_bg.wav'    # downloaded from mixkit
    mixer.init()
    mixer.music.load(bgMusic)
    mixer.music.play(-1)

bgMusic()
pygame.display.set_caption('Four In A Row - A Pratyush Inc Game')


def mainMenu():
    SQ_SIZE = 86 #length and the width of the square
    ROWS = 7
    COLUMNS = 7
    width = SQ_SIZE*ROWS
    height = SQ_SIZE*COLUMNS
    SCREEN = pygame.display.set_mode((width,height)) # make screen
    BLUE = (0, 0, 255) # blue color will be given once parameter is passed
    BLACK = (0, 0, 0) # black color will be given once parameter is passed
    RED = (255, 0, 0) # red color will be given once parameter is passed
    YELLOW = (255, 225, 0) # yellow color will be given once parameter is passed
    LIGHT_BLUE = (191, 239, 255) # light blue color will be given once parameter is passed
    WHITE = (255, 255, 255) # white will be given once parameter is passed
    ORANGE = (255, 128, 0) # orange will be given once parameter is passed
    DARK_ORANGE = (139,69,0) # dark orange will be given once parameter is passed
    RECT = (0, 0, width, height) # height needs to subtract SQ_SIZE
    # RADIUS = int((SQ_SIZE/2)-5)
    # STARTING_WIDTH = (SQ_SIZE/2)
    # STARTING_HEIGHT = int(SQ_SIZE + (SQ_SIZE/2))
    running=True

    # we are creating the light blue beginning menu
    def createMainMenu():
        mainMenu = pygame.draw.rect(SCREEN, LIGHT_BLUE, RECT)
        pygame.display.update()

    # we are creating the 4 buttons: easy, medium, hard to navigate in the game
    class buttons():
        def __init__(self, x, y, width, height, text, color):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.color = color
            self.coordinates = pygame.Rect(x,y,width,height) # this is capturing pygame property for each rectange

        def createButtons(self, SCREEN, OUTLINECOLOR=None):
            if OUTLINECOLOR:
                pygame.draw.rect(SCREEN, OUTLINECOLOR, (self.x-3,self.y-3,self.width+6,self.height+6),0,25,25,25,25)
            pygame.draw.rect(SCREEN, self.color, (self.x,self.y,self.width,self.height),0,25,25,25,25)


            font = pygame.font.SysFont(None, 40, bold=True, italic=False)
            text_image = font.render(self.text, True, BLACK)
            # SCREEN.blit(text_image,(self.x*2.5,self.y+SQ_SIZE*1/2))
            SCREEN.blit(text_image, (self.x + self.width/2 - text_image.get_width()/2, self.y + self.height/2 - text_image.get_height()/2))


        def isMouseOver(self, x, y):
            if self.coordinates.collidepoint(x,y): # x and y refers to the mouse points
                return True
            return False

        def changeButtonColor(self,color):
            self.color=color

    createMainMenu()

    multiPlayer = buttons(SQ_SIZE,0.5*SQ_SIZE,SQ_SIZE*5,SQ_SIZE,"MULTI-PLAYER", YELLOW)
    # multiPlayer.createButtons(SCREEN)

    cpuEasy = buttons(SQ_SIZE,SQ_SIZE*2,SQ_SIZE*5,SQ_SIZE,"CPU EASY", YELLOW)
    # cpuEasy.createButtons(SCREEN)

    cpuMedium = buttons(SQ_SIZE,SQ_SIZE*3.5,SQ_SIZE*5,SQ_SIZE,"CPU MEDIUM", YELLOW)
    # cpuMedium.createButtons(SCREEN)

    cpuHard = buttons(SQ_SIZE,SQ_SIZE*5,SQ_SIZE*5,SQ_SIZE,"CPU HARD", YELLOW)
    # cpuHard.createButtons(SCREEN)

    multiPlayer.createButtons(SCREEN, BLACK)
    cpuEasy.createButtons(SCREEN, BLACK)
    cpuMedium.createButtons(SCREEN, BLACK)
    cpuHard.createButtons(SCREEN, BLACK)

    while running == True:
        events = pygame.event.get()
        (x,y) = pygame.mouse.get_pos()
        for event in events:
            click = False
            # for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:
                if event.key==27:   # Esc = 27
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEMOTION:
                if multiPlayer.isMouseOver(x, y):
                    multiPlayer.changeButtonColor(ORANGE)
                else:
                    multiPlayer.changeButtonColor(YELLOW)

                if cpuEasy.isMouseOver(x, y):
                    cpuEasy.changeButtonColor(ORANGE)
                else:
                    cpuEasy.changeButtonColor(YELLOW)

                if cpuMedium.isMouseOver(x, y):
                    cpuMedium.changeButtonColor(ORANGE)
                else:
                    cpuMedium.changeButtonColor(YELLOW)

                if cpuHard.isMouseOver(x, y):
                    cpuHard.changeButtonColor(ORANGE)
                else:
                    cpuHard.changeButtonColor(YELLOW)





                pygame.display.update()



            if event.type == pygame.MOUSEBUTTONDOWN:
                if multiPlayer.isMouseOver(x, y):
                    multiPlayer.changeButtonColor(DARK_ORANGE)
                else:
                    multiPlayer.changeButtonColor(YELLOW)

                if cpuEasy.isMouseOver(x, y):
                    cpuEasy.changeButtonColor(DARK_ORANGE)
                else:
                    cpuEasy.changeButtonColor(YELLOW)

                if cpuMedium.isMouseOver(x, y):
                    cpuMedium.changeButtonColor(DARK_ORANGE)
                else:
                    cpuMedium.changeButtonColor(YELLOW)

                if cpuHard.isMouseOver(x, y):
                    cpuHard.changeButtonColor(DARK_ORANGE)
                else:
                    cpuHard.changeButtonColor(YELLOW)

            if event.type == pygame.MOUSEBUTTONUP:
                print(0)
                if event.button==1:
                    click=True
                    if multiPlayer.isMouseOver(x,y):
                        if click == True:
                            mp.multiPlayerRunning()

                    elif cpuEasy.isMouseOver(x,y):
                        if click == True:
                            ce.cpuEasy()

                    elif cpuMedium.isMouseOver(x,y):
                        if click == True:
                            cm.cpuMedium()

                    elif cpuHard.isMouseOver(x,y):
                        if click == True:
                            ch.cpuHard()

                    mainMenu()

            multiPlayer.createButtons(SCREEN, BLACK)
            cpuEasy.createButtons(SCREEN, BLACK)
            cpuMedium.createButtons(SCREEN, BLACK)
            cpuHard.createButtons(SCREEN, BLACK)

        pygame.display.update()


mainMenu()

#this is the main area where this project will run