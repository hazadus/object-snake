import random
import logging

from snake import Snake
from blocks import Block, Food


class Board:
    """
    Описывает игровое поле и логику взаимодействия объектов на нём - змейки, еды.

    __food: инстанс еды на игровом поле
    __snake: инстанс змейки
    __width: ширина игрового поля в блоках
    __height: высота игрового поля в блоках

    Args:
        board_width (int): в блоках
        board_height (int): в блоках

    """
    def __init__(self, board_width: int, board_height: int):
        self.__food = None
        self.__snake = None
        self.__width, self.__height = board_width, board_height
        self.reset()

    def food(self):
        """
        Возвращает текущий инстанс еды.

        :return: __food
        """
        return self.__food

    def snake(self):
        """
        Возвращает текущий инстанс змейки.

        :return: __snake
        """
        return self.__snake

    def width(self):
        """
        Возвращает ширину игрового поля в блоках.

        :return: __width
        """
        return self.__width

    def height(self):
        """
        Возвращает высоту игрового поля в блоках.

        :return: __height
        """
        return self.__height

    def respawn_snake(self):
        """
        Убивает змейку (при наличии) и создаёт новую - одна голова по центру поля.
        """
        if self.__snake is not None:
            self.__snake.kill()

        self.__snake = Snake(x=int(self.width() / 2), y=int(self.height() / 2))

    def respawn_food(self):
        """
        Создаёт инстанс еды на месте случайного блока, не занятого змейкой.
        """
        all_free_blocks = [Block(i, j) for i in range(self.width())
                           for j in range(self.height())
                           if not Block(i, j) in self.snake().blocks()]
        self.__food = Food(random.choice(all_free_blocks))
        logging.info(f'New food at({self.__food.x()},{self.__food.y()})')

    def reset(self):
        """
        Сбрасывает игровое поле – респавнит змейку и еду.
        """
        self.respawn_snake()
        self.respawn_food()
        logging.info('Board reset.')

    def make_move(self) -> tuple:
        """
        Обработка хода змейки в установленном направлении - проверяет возможные коллизии и даёт команды змейке на
        движение, поедание еды.

        :return: кортеж (bool - жива ли змейка, int - сколь заработано очков за ход)
        """
        next_x, next_y = self.snake().predict_head_position()
        next_x %= self.width()
        next_y %= self.height()
        next_block = Block(next_x, next_y)
        add_points = 0
        is_alive = True

        if self.food() == next_block:  # food met!
            self.snake().move_to(next_x, next_y)
            add_points = self.snake().eat(self.food())
            self.respawn_food()
        elif next_block in self.snake().blocks():  # collision with tail!
            is_alive = False
        else:
            self.snake().move_to(next_x, next_y)

        return is_alive, add_points
