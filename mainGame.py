import pygame
import sys
from pygame.locals import *
from colors import *


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

BRICK_WIDTH = 60
BRICK_HEIGHT = 15
PADDLE_WIDTH = 60
PADDLE_HEIGHT = 12
BALL_DIAMETER = 16
BALL_RADIUS = BALL_DIAMETER / 2

MAX_PADDLE_X = WINDOW_WIDTH - PADDLE_WIDTH
MAX_BALL_X = WINDOW_WIDTH - BALL_DIAMETER
MAX_BALL_Y = WINDOW_HEIGHT - BALL_DIAMETER

PADDLE_Y = WINDOW_HEIGHT - PADDLE_HEIGHT - 10

# states

S_BALL_ON_PADDLE = 0
S_PLAY = 1
S_WON = 2
S_END_GAME = 3

class Main:
    def __init__(self):
        pygame.init()

        self.create_window()

        self.clock = pygame.time.Clock()
        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

        self.create_game()

    def create_window(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Double Arkanoid')

    def create_game(self):
        self.lives = 3
        self.score = 0
        self.state = S_BALL_ON_PADDLE

        self.paddle = pygame.Rect(300, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(300, PADDLE_Y - BALL_DIAMETER, BALL_DIAMETER, BALL_DIAMETER)  # zastanowic sie jak mozna zrobic kulke

        self.ball_vel = [5, -5]

        self.create_bricks()

    def create_bricks(self):
        position_y = 35
        self.bricks = []
        for i in range(7):
            position_x = 35
            for j in range(8):
                self.bricks.append(pygame.Rect(position_x, position_y, BRICK_WIDTH, BRICK_HEIGHT))
                position_x += BRICK_WIDTH + 10
            position_y += BRICK_HEIGHT + 5

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BOTTOM_PADDLE_COLOR, brick)

    def check_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.left -= 5
            if self.paddle.left < 0:
                self.paddle.left = 0
        if keys[pygame.K_RIGHT]:
            self.paddle.right += 5
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == S_BALL_ON_PADDLE:
            self.ball_vel = [5, -5]
            self.state = S_PLAY
        elif keys[pygame.K_RETURN] and (self.state == S_END_GAME or self.state == S_WON):
            self.create_game()

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
            self.ball_vel[1] = -self.ball_vel[1]

    def collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break

        if len(self.bricks) == 0:
            self.state = S_WON

        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = S_BALL_ON_PADDLE
            else:
                self.state = S_END_GAME

    def show_stats(self):
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, WHITE)
            self.screen.blit(font_surface, (205, 5))

    def show_message(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, WHITE)
            x = (WINDOW_WIDTH - size[0]) / 2
            y = (WINDOW_HEIGHT - size[1]) / 2
            self.screen.blit(font_surface, (x, y))

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(50)
            self.screen.fill(BGCOLOR)
            self.check_input()

            if self.state == S_PLAY:
                self.move_ball()
                self.collisions()
            elif self.state == S_BALL_ON_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO PLAY")
            elif self.state == S_END_GAME:
                self.show_message("GAME OVER")
            elif self.state == S_WON:
                self.show_message("YOU WON!")

            self.draw_bricks()
            pygame.draw.rect(self.screen, BOTTOM_PADDLE_COLOR, self.paddle)
            pygame.draw.circle(self.screen, WHITE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)

            self.show_stats()

            pygame.display.update()
        # self.gameSurface = self.create_window()

        # self.main_loop()
    #

    #
    # def main_loop(self):
    #     self.gameSurface.fill(BGCOLOR)

if __name__ == "__main__":
    Main().run()
