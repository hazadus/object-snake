import logging

import pygame

from config import Config
from snake import Snake
from game import Game


class Engine:
    """
    Описывает состояния и функционал "игрового движка".
    Получение ввода от игрока, вывод картинки на экран.

    Args:
        config (Config): инстанс конфигурации игры

    """
    # States
    state_menu, state_game, state_gameover, state_enter_highscore = range(4)
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

    def __init__(self, config: Config):
        self.__config = config
        self.__state = self.state_menu
        self.__block_size = config['block_size']  # размер одного блока в пикселях
        self.__margin_top = config['margin_top']
        self.__base_speed = config['base_speed']

        pygame.init()

        self.__game = Game(config['board_width'], config['board_height'], config['player_name'])
        self.__window_width = self.__game.board().width() * self.__block_size
        self.__window_height = self.__margin_top + self.__game.board().height() * self.__block_size
        self.__display = pygame.display.set_mode((self.__window_width, self.__window_height))
        pygame.display.set_caption(config['window_caption'])
        self.__clock = pygame.time.Clock()
        logging.info(f'New game initialized: {config["window_caption"]}, {self.__window_width}x{self.__window_height}')

    @staticmethod
    def quit():
        """
        Завершает работу библиотеки pygame и программы в целом.
        """
        pygame.quit()
        quit()

    def draw_frame(self):
        """
        Отрисовывает один кадр игры и выводит его на экран.
        Один кадр на один игровой ход. После отрисовки производится задержка, определяющая скорость игры.
        """
        font_logo_name = self.__config['font_logo_name']
        font_info_line_name = self.__config['font_info_line_name']
        font_paused_name = self.__config['font_paused_name']
        str_logo = 'SNAKE'
        str_paused = '* PAUSE *'
        str_game_over = 'Game Over!'

        self.__display.fill(self.color_background)

        # МЕНЮ - show 'logo'
        if self.__state == self.state_menu:
            font_logo = pygame.font.SysFont(font_logo_name, 100)
            surf_logo = font_logo.render(str_logo, True, self.color_info_line_text)
            logo_width, logo_height = font_logo.size(str_logo)
            self.__display.blit(surf_logo, [int((self.__window_width - logo_width) / 2),
                                            int((self.__window_height - logo_height) / 2)])

        # ИГРА или ГЕЙМОВЕР
        if self.__state == self.state_game or self.__state == self.state_gameover:
            # Отрисовываем змейку
            for block in self.__game.board().snake().blocks():
                pygame.draw.rect(self.__display,
                                 self.red if block.is_head() else self.blue,
                                 [block.x() * self.__block_size,
                                  self.__margin_top + block.y() * self.__block_size,
                                  self.__block_size, self.__block_size])

            # Отрисовываем еду
            pygame.draw.rect(self.__display, self.green,
                             [self.__game.board().food().x() * self.__block_size,
                              self.__margin_top + self.__game.board().food().y() * self.__block_size,
                              self.__block_size, self.__block_size])

            # Show info line at the top of the window
            # 1) draw rect for top info line
            pygame.draw.rect(self.__display, self.color_top_info_line, [0, 0, self.__window_width, self.__margin_top])
            font_info_line = pygame.font.SysFont(font_info_line_name, 20)
            # 2) level
            str_level = f'LVL {self.__game.level()}'
            surf_level = font_info_line.render(str_level, True, self.color_info_line_text)
            level_width, level_height = font_info_line.size(str_level)
            self.__display.blit(surf_level, [int((self.__window_width / 3 - level_width) / 2),
                                             int((self.__margin_top - level_height) / 2)])
            # 3) score
            str_score = str(self.__game.score())
            surf_score = font_info_line.render(str_score, True, self.black)
            score_width, score_height = font_info_line.size(str_score)
            self.__display.blit(surf_score, [int((self.__window_width - score_width) / 2),
                                             int((self.__margin_top - score_height) / 2)])
            # 4) head (x,y)
            str_xy = f'(x:{self.__game.board().snake().head().x()}, y:{self.__game.board().snake().head().y()})'
            surf_xy = font_info_line.render(str_xy, True, self.gray)
            xy_width, xy_height = font_info_line.size(str_xy)
            self.__display.blit(surf_xy, [int(self.__window_width / 3 * 2 + (self.__window_width / 3 - xy_width) / 2),
                                          int((self.__margin_top - xy_height) / 2)])
            # Если игра на паузе, но не геймовер - выводим надпись "пауза" на экране
            if self.__game.is_paused() and not self.__game.is_gameover():
                font_paused = pygame.font.SysFont(font_paused_name, 75)
                surf_paused = font_paused.render(str_paused, True, self.red)
                paused_width, paused_height = font_paused.size(str_paused)
                self.__display.blit(surf_paused, [int((self.__window_width - paused_width) / 2),
                                                  int((self.__window_height - paused_height) / 2)])

        # GAMEOVER screen
        if self.__state == self.state_gameover:
            font_logo = pygame.font.SysFont(font_logo_name, 60)
            surf_logo = font_logo.render(str_game_over, True, self.red)
            logo_width, logo_height = font_logo.size(str_game_over)
            self.__display.blit(surf_logo, [int((self.__window_width - logo_width) / 2),
                                            int((self.__window_height - logo_height) / 2)])

        # Вывод на экран + задержка в зависимости от уровня игры
        pygame.display.update()
        self.__clock.tick(self.__base_speed + self.__game.level())

    def game_loop(self):
        """
        Цикл событий игры. Получаем ввод от игрока, реагируем на него, по результатм отрисовываем очередной кадр.
        По выходу из цикла, игра завершается.
        """
        while not self.__game.is_quit():
            for event in pygame.event.get():
                # Реагируем на закрытие окна - завершаем игру
                if event.type == pygame.QUIT:
                    self.__game.quit()
                # STATES
                # MENU
                if self.__state == self.state_menu:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.__state = self.state_game
                        elif event.key == pygame.K_ESCAPE:
                            self.__game.quit()
                # GAME OVER
                elif self.__state == self.state_gameover:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.__state = self.state_menu
                            self.__game.reset()
                        elif event.key == pygame.K_ESCAPE:
                            self.__game.quit()
                # GAME
                elif self.__state == self.state_game:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.__game.board().snake().set_direction(Snake.direction_right)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.__game.board().snake().set_direction(Snake.direction_down)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.__game.board().snake().set_direction(Snake.direction_left)
                        elif event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.__game.board().snake().set_direction(Snake.direction_up)
                        elif event.key == pygame.K_SPACE:
                            self.__game.toggle_pause()
                        elif event.key == pygame.K_ESCAPE:
                            self.__state = self.state_gameover
                            self.__game.game_over()

            if self.__state == self.state_game:
                self.__game.make_turn()
                if self.__game.is_gameover():
                    self.__state = self.state_gameover

            self.draw_frame()
