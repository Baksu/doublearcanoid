import pygame
import mainGame
from colors import *

PADDLE_WIDTH = 60
PADDLE_HEIGHT = 12
BALL_DIAMETER = 16
BALL_RADIUS = BALL_DIAMETER / 2

MAX_PADDLE_X = mainGame.PLAYGROUND_WIDTH - PADDLE_WIDTH


class Player:
    def __init__(self, screen,  paddle_y_position):
        self.screen = screen
        self.paddle = pygame.Rect(300, paddle_y_position, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(300, paddle_y_position - BALL_DIAMETER, BALL_DIAMETER, BALL_DIAMETER)
        self.ball_vel = [5, -5]

        self.score = 0

    def draw_player(self, color):
        pygame.draw.rect(self.screen, color, self.paddle)

    def move_left(self):
        self.paddle.left -= 5
        if self.paddle.left < 0:
            self.paddle.left = 0

    def move_right(self):
        self.paddle.right += 5
        if self.paddle.left > MAX_PADDLE_X:
            self.paddle.left = MAX_PADDLE_X
