import random

from snake import Snake
from blocks import Block


class Board:
    def __init__(self, board_width: int, board_height: int):
        self.food = None
        self.snake = None
        self.width, self.height = board_width, board_height
        self.respawn_snake()
        self.respawn_food()

    def respawn_snake(self):
        self.snake = Snake(int(self.width / 2),
                           int(self.height / 2))

    def respawn_food(self):
        all_free_blocks = [Block(i, j) for i in range(self.width)
                           for j in range(self.height)
                           if not Block(i, j) in self.snake.blocks]
        self.food = random.choice(all_free_blocks)

    def make_move(self):
        """
        Проверяет возможные коллизии и даёт команды змейке на движение, поедание еды.
        :return:
        """
        # TODO: check for collisions with walls or tail
        next_x, next_y = self.snake.predict_head_position()
        next_x %= self.width
        next_y %= self.height
        next_block = Block(next_x, next_y)
        if self.food == next_block:
            self.snake.eat(self.food)
            self.respawn_food()
        self.snake.move_to(next_x, next_y)


class Game:
    is_gameover = False
    is_paused = False
    score = 0
    level = 1

    # score_up()
    # hiscore, or high scores table
    def __init__(self, board_width: int, board_height: int):
        """
        :param board_width: ширина игрового поля (в блоках)
        :param board_height: высота игрового поля (в блоках)
        """
        self.board = Board(board_width, board_height)

    def game_over(self):
        self.is_gameover = True

    def make_move(self):
        if not self.is_paused:
            self.board.make_move()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
