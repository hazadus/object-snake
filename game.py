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


class Game:
    is_gameover = False
    is_paused = False
    is_quit = False
    score = 0
    level = 1

    def __init__(self, board_width: int, board_height: int):
        """
        :param board_width: ширина игрового поля (в блоках)
        :param board_height: высота игрового поля (в блоках)
        """
        self.board = Board(board_width, board_height)

    def reset(self):
        self.is_gameover = False
        self.is_paused = False
        self.score = 0
        self.level = 1
        self.board.reset()

    def game_over(self):
        self.is_gameover = True

    def quit(self):
        self.is_quit = True

    def make_move(self):
        """
        Двигает змейку, и проверяет - съест ли она еду (и сколько очков заработает), убьется ли
        (и завершает игру в данном случае), при необходимости увеличивает "уровень".
        :return:
        """
        if not self.is_paused:
            is_alive, add_points = self.board.make_move()
            self.score += add_points
            if add_points:
                logging.info(f'Score: {self.score}, snake length: {len(self.board.snake.blocks)}')

            if self.score >= self.level*100:
                self.level += 1

            if not is_alive:
                self.game_over()
                logging.info('Game over!')

    def toggle_pause(self):
        self.is_paused = not self.is_paused
