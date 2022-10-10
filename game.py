import logging

from board import Board
from highscores import Highscores, Score


class Game:
    highscores = None
    is_gameover = False
    is_paused = False
    is_quit = False
    score = 0
    level = 1

    def __init__(self, board_width: int, board_height: int, default_player_name: str):
        """
        :param board_width: ширина игрового поля (в блоках)
        :param board_height: высота игрового поля (в блоках)
        """
        self.board = Board(board_width, board_height)
        self.default_player_name = default_player_name
        self.highscores = Highscores()
        self.reset()

    def reset(self):
        self.is_gameover = False
        self.is_paused = False
        self.score = 0
        self.level = 1
        self.board.reset()

    def game_over(self):
        self.highscores.save()
        self.is_gameover = True

    def quit(self):
        self.is_quit = True

    def make_turn(self):
        """
        Двигает змейку, и проверяет - съест ли она еду (и сколько очков заработает), убьется ли
        (и завершает игру в данном случае), при необходимости увеличивает "уровень".
        :return:
        """
        if not self.is_paused:
            is_alive, add_points = self.board.make_move()
            self.score += add_points
            if add_points:
                logging.info(f'Score: {self.score}, snake length: {len(self.board.snake)}')

            if self.score >= self.level*100:
                self.level += 1

            if not is_alive:
                score = Score(self.default_player_name, self.score)
                self.highscores.add(score)
                self.game_over()
                logging.info('Game over!')

    def toggle_pause(self):
        self.is_paused = not self.is_paused
