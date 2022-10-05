import random

from snake import Snake
from food import Food


class Board:
    # spawn food()
    # food
    # move snake (check collision) - ?
    # move snake here?
    def __init__(self, board_width: int, board_height: int):
        self.food = None
        self.snake = None
        self.width, self.height = board_width, board_height
        self.respawn_snake()
        self.respawn_food()

    def respawn_snake(self):
        self.snake = Snake(int(self.width/2),
                           int(self.height/2))

    def respawn_food(self):
        # TODO: check if block is clear
        self.food = Food(random.randint(0, self.width), random.randint(0, self.height))

    def make_move(self):
        # TODO: check for collisions with walls or tail
        next_x, next_y = self.snake.predict_head_position()
        if self.food.x == next_x and self.food.y == next_y:
            self.snake.eat(self.food)
            self.respawn_food()
            self.snake.make_move()
        else:
            self.snake.make_move()


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
