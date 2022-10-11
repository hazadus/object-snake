import logging

from board import Board
from highscores import Highscores, Score


class Game:
    """
    Описывает объект игры, с её состояниями и параметрами.

    __board: инстанс объекта игрового поля класса Board
    __default_player_name: имя игрока по умолчанию
    __highscores: инстанс объекта таблицы рекордов класса Highscores
    __is_gameover: флаг геймовера
    __is_paused: флаг паузы
    __is_quit: флаг завершения игры
    __score (int): текущий счет в очках
    __level (int): текущий уровень

    Args:
        board_width (int): ширина игрового поля в блоках
        board_height (int): высота игрового поля в блоках
        default_player_name (str): имя игрока по умолчанию (для сохранения рекордов)

    """
    def __init__(self, board_width: int, board_height: int, default_player_name: str):
        self.__board = Board(board_width, board_height)
        self.__default_player_name = default_player_name
        self.__highscores = Highscores()
        self.__is_gameover = False
        self.__is_paused = False
        self.__is_quit = False
        self.__score = 0
        self.__level = 1

        self.reset()

    def board(self):
        """
        Возвращает инстанс объекта игрового поля.

        :return: __board
        """
        return self.__board

    def highscores(self):
        """
        Возвращает инстанс объекта таблицы рекордов.

        :return: __highscores
        """
        return self.__highscores

    def is_gameover(self):
        """
        Возвращает состояние флага геймовера.

        :return: __is_gameover
        """
        return self.__is_gameover

    def is_paused(self):
        """
        Возвращает состояние флага паузы.

        :return: __is_paused
        """
        return self.__is_paused

    def is_quit(self):
        """
        Возвращает состояние флага завершения игры.

        :return: __is_quit
        """
        return self.__is_quit

    def score(self) -> int:
        """
        Возвращает текущий счет.

        :return: __score
        """
        return self.__score

    def score_add_points(self, add_points: int):
        """
        Увеличивает текущий счет на передаваемое значение.

        :param add_points: сколько добавить очков
        """
        self.__score += add_points

    def level(self):
        """
        Возвращает текущий уровень.

        :return: __level
        """
        return self.__level

    def level_up(self):
        """
        Увеличивает уровень при соответствии прописанному условию.
        """
        if self.score() >= self.level() * 100:
            self.__level += 1

    def reset(self):
        """
        Сброс состояния игры до начального.
        """
        self.__is_gameover = False
        self.__is_paused = False
        self.__score = 0
        self.__level = 1
        self.board().reset()

    def game_over(self):
        """
        Перевести игры в состояние геймовера, добавить и сохранить текущий счет в таблице рекордов.
        """
        score = Score(self.__default_player_name, self.score())
        self.highscores().add(score)
        self.highscores().save()
        self.__is_gameover = True

    def quit(self):
        """
        Перевести игру в состояние выхода из игры.
        """
        self.__is_quit = True

    def make_turn(self):
        """
        Двигает змейку, и проверяет - съест ли она еду (и сколько очков заработает), убьется ли
        (и завершает игру в данном случае), при необходимости увеличивает уровень.
        """
        if not self.is_paused():
            is_alive, add_points = self.board().make_move()
            self.score_add_points(add_points)
            if add_points:
                logging.info(f'Score: {self.score()}, snake length: {len(self.board().snake())}')

            self.level_up()

            if not is_alive:
                self.game_over()
                logging.info('Game over!')

    def toggle_pause(self):
        """
        Переключает флаг паузы игры.
        """
        self.__is_paused = not self.__is_paused
