import pygame
import mainGame
from colors import *

PADDLE_WIDTH = 60
PADDLE_HEIGHT = 12
BALL_DIAMETER = 16
BALL_RADIUS = BALL_DIAMETER / 2

MAX_PADDLE_X = mainGame.PLAYGROUND_WIDTH - PADDLE_WIDTH
MAX_BALL_X = mainGame.PLAYGROUND_WIDTH - BALL_DIAMETER
MAX_BALL_Y = mainGame.PLAYGROUND_HEIGHT - BALL_DIAMETER

#player_posiotn
UP_PLAYER = 1
DOWN_PLAYER = 0

POINTS_FOR_HIT_GROUND = -100

class Player:
    def __init__(self, screen,  paddle_y_position, player_position):
        self.paddle_y_position = paddle_y_position
        self.player_position = player_position
        self.screen = screen
        self.paddle = pygame.Rect(300, paddle_y_position, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(300, paddle_y_position - BALL_DIAMETER, BALL_DIAMETER, BALL_DIAMETER)
        if self.player_position == DOWN_PLAYER:
            self.ball_vel = [5, -5]
        else:
            self.ball_vel = [5, 5]

        self.score = 0

    def move_left(self):
        self.paddle.left -= 5
        if self.paddle.left < 0:
            self.paddle.left = 0

    def move_right(self):
        self.paddle.right += 5
        if self.paddle.left > MAX_PADDLE_X:
            self.paddle.left = MAX_PADDLE_X

    def play_game(self):
        self.move_ball()

    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]

        if self.ball.top < 0:
            self.ball.top = 0
            self.switch_ball_vertical()
        elif self.ball.bottom > mainGame.PLAYGROUND_HEIGHT:
            self.ball.bottom = mainGame.PLAYGROUND_HEIGHT
            self.switch_ball_vertical()

    def move_ball_on_paddle(self):
        self.ball.left = self.paddle.left + self.paddle.width / 2
        if self.player_position == DOWN_PLAYER:
            self.ball.top = self.paddle.top - self.ball.height
        else:
            self.ball.top = self.paddle.top + self.ball.height

    def draw_player(self, color):
        self.player_color = color
        self.draw_paddle()
        self.draw_ball()

    def draw_paddle(self):
        pygame.draw.rect(self.screen, self.player_color, self.paddle)

    def draw_ball(self):
        pygame.draw.circle(self.screen, self.player_color, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)

    def get_ball(self):
        return self.ball

    def add_score(self, points):
        self.score += points

    def switch_ball_vertical(self):
        self.ball_vel[1] = -self.ball_vel[1]

    def check_ball_paddle_collision(self):
        if self.ball.colliderect(self.paddle):
            if self.player_position == DOWN_PLAYER:
                self.ball.top = self.paddle_y_position - BALL_DIAMETER
            else:
                self.ball.top = self.paddle_y_position + PADDLE_HEIGHT
            self.switch_ball_vertical()

    def check_ball_ground_collision(self):
        if self.ball.top > self.paddle.top:
            self.ball_hit_ground()

    def ball_hit_ground(self):
        self.add_score(POINTS_FOR_HIT_GROUND)
