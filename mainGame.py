import pygame
import sys
import player
from pygame.locals import *
from colors import *


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

PLAYGROUND_WIDTH = 640
PLAYGROUND_HEIGHT = 1000

BRICK_WIDTH = 60
BRICK_HEIGHT = 15

POINTS_FOR_BRICK = 10

S_BALLS_ON_PADDLE = 0
S_PLAY = 1
S_WON = 2
S_END_GAME = 3

class Main:
    def __init__(self):
        pygame.init()

        self.create_window()
        self.create_playground()

        self.clock = pygame.time.Clock()
        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None

        self.create_game()

    def create_window(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Double Arkanoid')

    def create_playground(self):
        self.playground = pygame.Rect(0, 0, PLAYGROUND_WIDTH, PLAYGROUND_HEIGHT)

    def create_game(self):
        self.state = S_BALLS_ON_PADDLE
        self.create_players()
        self.create_bricks()

    def create_players(self):
        down_paddle_y = PLAYGROUND_HEIGHT - player.PADDLE_HEIGHT - 10
        self.player_down = player.Player(self.screen, down_paddle_y, player.DOWN_PLAYER)
        up_paddle_y = player.PADDLE_HEIGHT + 10
        self.player_up = player.Player(self.screen, up_paddle_y, player.UP_PLAYER)

    def create_bricks(self):
        position_y = 1000/2 - 3 * BRICK_HEIGHT - BRICK_HEIGHT/2
        self.bricks = []
        for i in range(7):
            position_x = 35
            for j in range(8):
                self.bricks.append(pygame.Rect(position_x, position_y, BRICK_WIDTH, BRICK_HEIGHT))
                position_x += BRICK_WIDTH + 10
            position_y += BRICK_HEIGHT + 5

    def draw_playground(self):
        self.screen.fill(BGCOLOR)
        pygame.draw.rect(self.screen, PLAYGROUND, self.playground)
        self.player_down.draw_player(DOWNPLAYERCOLOR)
        self.player_up.draw_player(UPPLAYERCOLOR)
        self.draw_bricks()

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BOTTOM_PADDLE_COLOR, brick)

    def check_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_down.move_left()
        if keys[pygame.K_RIGHT]:
            self.player_down.move_right()
        if keys[pygame.K_z]:
            self.player_up.move_left()
        if keys[pygame.K_c]:
            self.player_up.move_right()

        if keys[pygame.K_SPACE] and self.state == S_BALLS_ON_PADDLE:
            self.state = S_PLAY
        # elif keys[pygame.K_RETURN] and (self.state == S_END_GAME or self.state == S_WON):
        #     self.create_game()

    #
    def check_collisions(self, player):
        ball = player.get_ball()
        for brick in self.bricks:
            if ball.colliderect(brick):
                player.add_score(POINTS_FOR_BRICK)
                player.switch_ball_vertical()
                self.bricks.remove(brick)
                break
        player.check_ball_paddle_collision()
        player.check_ball_ground_collision()

    #
    # def show_stats(self):
    #     if self.font:
    #         font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, WHITE)
    #         self.screen.blit(font_surface, (205, 5))
    #
    def show_message(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, WHITE)
            x = PLAYGROUND_WIDTH + 10
            y = (WINDOW_HEIGHT - size[1]) / 2
            self.screen.blit(font_surface, (x, y))

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(50)
            self.draw_playground()
            self.check_input()
            self.check_collisions(self.player_up)
            self.check_collisions(self.player_down)

            # if len(self.bricks) == 0:  ADD END GAME
            #     self.state = S_WON

            if self.state == S_PLAY:
                self.player_up.play_game()
                self.player_down.play_game()
            elif self.state == S_BALLS_ON_PADDLE:
                self.player_up.move_ball_on_paddle()
                self.player_down.move_ball_on_paddle()
                self.show_message("PRESS SPACE TO PLAY")
            # elif self.state == S_END_GAME:
                # self.show_message("GAME OVER")
            # elif self.state == S_WON:
                # self.show_message("YOU WON!")

            # self.show_stats()

            pygame.display.update()

if __name__ == "__main__":
    Main().run()
