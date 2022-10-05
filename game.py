from snake import Snake


class Board:
    # spawn food()
    # food
    # move snake (check collision) - ?
    # move snake here?
    pass


class Game:
    is_gameover = False
    score = 0
    level = 1
    snake = None

    # score_up()
    # hiscore, or high scores table
    def __init__(self, board_width: int, board_height: int):
        """
        :param board_width: ширина игрового поля (в блоках)
        :param board_height: высота игрового поля (в блоках)
        """
        self.board_width = board_width
        self.board_height = board_height
        self.respawn_snake()

    def game_over(self):
        self.is_gameover = True

    def respawn_snake(self):
        self.snake = Snake(1, 1)
