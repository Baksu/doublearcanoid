import pygame
import sys
from pygame.locals import *
from colors import *


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

class Main:
    def __init__(self):
        pygame.init()
        self.gameSurface = self.create_scene()

    def create_scene(self):
        pygame.display.set_caption('Double Arkanoid')
        gameSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        gameSurface.fill(BGCOLOR)
        gameSurface.convert()
        return gameSurface

    def main_loop(self):
        self.gameSurface.fill(BGCOLOR)

startGame = Main()
startGame.main_loop()
