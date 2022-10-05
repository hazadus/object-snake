import pygame


class SnakeBlock:
    # x
    # y
    # is_head
    pass


class Snake:
    # length
    # blocks list
    # head
    # speed
    # direction
    #
    # move()
    # change_direction()
    # grow()
    pass


class Food:
    # x
    # y
    pass


class Game:
    is_gameover = False
    score = 0
    level = 1

    # score_up()
    # hiscore, or high scores table
    def __init__(self, board_width: int, board_height: int):
        """
        :param board_width: ширина игрового поля (в блоках)
        :param board_height: высота игрового поля (в блоках)
        """
        self.board_width = board_width
        self.board_height = board_height

    def game_over(self):
        self.is_gameover = True


class Engine:
    def __init__(self, window_width: int, window_height: int, window_caption: str):
        pygame.init()
        self.display = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(window_caption)

    def quit(self):
        pygame.quit()
        quit()

    def update(self):
        pygame.display.update()


if __name__ == '__main__':
    engine = Engine(600, 600, 'Object Snake')
    game = Game(60, 60)

    while not game.is_gameover:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                game.game_over()

    engine.update()
    engine.quit()
