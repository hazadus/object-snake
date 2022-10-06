import logging

import pygame

from snake import Snake
from game import Game


class Engine:
    # States
    state_menu = 1
    state_game = 2
    state_gameover = 3
    state_enter_highscore = 4
    state = state_menu
    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 102)
    green = (0, 153, 51)
    blue = (0, 102, 255)
    gray = (102, 102, 153)
    color_top_info_line = (204, 153, 255)
    color_info_line_text = (0, 51, 153)
    color_background = (204, 204, 255)
    # Sizes
    margin_top = 25
    block_size = 17  # размер одного блока в пикселях
    base_speed = 5

    def __init__(self, game: Game, window_caption: str):
        pygame.init()
        self.game = game
        self.window_width = game.board.width * self.block_size
        self.window_height = self.margin_top + game.board.height * self.block_size
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(window_caption)
        self.clock = pygame.time.Clock()
        logging.info(f'New game initialized: {window_caption}, {self.window_width}x{self.window_height}')

    def quit(self):
        pygame.quit()
        quit()

    def draw_frame(self):
        self.display.fill(self.color_background)

        if self.state == self.state_menu:
            # Menu - show 'logo'
            font_logo = pygame.font.SysFont("PT Mono", 100)
            str_logo = 'SNAKE'
            surf_logo = font_logo.render(str_logo, True, self.color_info_line_text)
            logo_width, logo_height = font_logo.size(str_logo)
            self.display.blit(surf_logo, [int((self.window_width - logo_width) / 2),
                                          int((self.window_height - logo_height) / 2)])

        if self.state == self.state_game or self.state == self.state_gameover:
            # Render snake
            for block in self.game.board.snake.blocks:
                pygame.draw.rect(self.display,
                                 self.red if block.is_head else self.blue,
                                 [block.x * self.block_size,
                                  self.margin_top + block.y * self.block_size,
                                  self.block_size, self.block_size])

            # Render food
            pygame.draw.rect(self.display, self.green,
                             [self.game.board.food.x * self.block_size,
                              self.margin_top + self.game.board.food.y * self.block_size,
                              self.block_size, self.block_size])

            # Show info line at the top of the window
            # 1) draw rect for top info line
            pygame.draw.rect(self.display, self.color_top_info_line, [0, 0, self.window_width, self.margin_top])
            font_info_line = pygame.font.SysFont("PT Mono", 20)
            # 2) level
            str_level = f'LVL {self.game.level}'
            surf_level = font_info_line.render(str_level, True, self.color_info_line_text)
            level_width, level_height = font_info_line.size(str_level)
            self.display.blit(surf_level, [int((self.window_width / 3 - level_width) / 2),
                                           int((self.margin_top - level_height) / 2)])
            # 3) score
            str_score = str(self.game.score)
            surf_score = font_info_line.render(str_score, True, self.black)
            score_width, score_height = font_info_line.size(str_score)
            self.display.blit(surf_score, [int((self.window_width - score_width) / 2),
                                           int((self.margin_top - score_height) / 2)])
            # 4) head (x,y)
            str_xy = f'(x:{self.game.board.snake.head.x}, y:{self.game.board.snake.head.y})'
            surf_xy = font_info_line.render(str_xy, True, self.gray)
            xy_width, xy_height = font_info_line.size(str_xy)
            self.display.blit(surf_xy, [int(self.window_width / 3 * 2 + (self.window_width / 3 - xy_width) / 2),
                                        int((self.margin_top - xy_height) / 2)])
            # 5) paused?
            if self.game.is_paused:
                font_paused = pygame.font.SysFont("Chalkboard", 75)
                str_paused = '* PAUSE *'
                surf_paused = font_paused.render(str_paused, True, self.red)
                paused_width, paused_height = font_paused.size(str_paused)
                self.display.blit(surf_paused, [int((self.window_width - paused_width) / 2),
                                                int((self.window_height - paused_height) / 2)])

        if self.state == self.state_gameover:
            # Game over screen
            font_logo = pygame.font.SysFont("PT Mono", 60)
            str_logo = 'Game Over!'
            surf_logo = font_logo.render(str_logo, True, self.red)
            logo_width, logo_height = font_logo.size(str_logo)
            self.display.blit(surf_logo, [int((self.window_width - logo_width) / 2),
                                          int((self.window_height - logo_height) / 2)])

        pygame.display.update()
        self.clock.tick(self.base_speed + self.game.level)

    def game_loop(self):
        while not self.game.is_quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.quit()
                # STATES
                # MENU
                if self.state == self.state_menu:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.state = self.state_game
                        elif event.key == pygame.K_ESCAPE:
                            self.game.quit()
                # GAME OVER
                elif self.state == self.state_gameover:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.state = self.state_menu
                            self.game.reset()
                        elif event.key == pygame.K_ESCAPE:
                            self.game.quit()
                # GAME
                elif self.state == self.state_game:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            self.game.board.snake.set_direction(Snake.direction_right)
                        elif event.key == pygame.K_DOWN:
                            self.game.board.snake.set_direction(Snake.direction_down)
                        elif event.key == pygame.K_LEFT:
                            self.game.board.snake.set_direction(Snake.direction_left)
                        elif event.key == pygame.K_UP:
                            self.game.board.snake.set_direction(Snake.direction_up)
                        elif event.key == pygame.K_SPACE:
                            self.game.toggle_pause()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = self.state_gameover

            if self.state == self.state_game:
                self.game.make_move()
                if self.game.is_gameover:
                    self.state = self.state_gameover

            self.draw_frame()
