import random
import logging

from snake import Snake
from blocks import Block, Food


class Board:
    def __init__(self, board_width: int, board_height: int):
        self.food = None
        self.snake = None
        self.width, self.height = board_width, board_height
        self.reset()

    def respawn_snake(self):
        if self.snake is not None:
            self.snake.kill()

        self.snake = Snake(int(self.width / 2),
                           int(self.height / 2))

    def respawn_food(self):
        all_free_blocks = [Block(i, j) for i in range(self.width)
                           for j in range(self.height)
                           if not Block(i, j) in self.snake.blocks]
        self.food = random.choice(all_free_blocks)
        logging.info(f'New food at({self.food.x},{self.food.y})')

    def reset(self):
        self.respawn_snake()
        self.respawn_food()
        logging.info('Board reset.')

    def make_move(self) -> tuple:
        """
        Проверяет возможные коллизии и даёт команды змейке на движение, поедание еды.
        :return: (bool - жива ли змейка, int - сколь заработано очков за ход)
        """
        next_x, next_y = self.snake.predict_head_position()
        next_x %= self.width
        next_y %= self.height
        next_block = Block(next_x, next_y)
        add_points = 0
        is_alive = True

        if self.food == next_block:  # food met!
            self.snake.move_to(next_x, next_y)
            self.snake.eat(self.food)
            self.respawn_food()
            add_points = Food.points
        elif next_block in self.snake.blocks:  # collision with tail!
            is_alive = False
        else:
            self.snake.move_to(next_x, next_y)

        return is_alive, add_points
