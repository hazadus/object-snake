from game import Game
from engine import Engine


# Engine - renders game objects
#
# Game                  - score, level
#   Board               - size, borders | spawn snake & food, check collisions -> move snake
#       Food            - x, y
#       Snake           - blocks, direction, head | eat, grow, move (w/o collision check)
#                       - represent snake as 'tree'
#           SnakeBlock  - x, y, is_head?

class Food:
    # x
    # y
    pass


if __name__ == '__main__':
    the_game = Game(60, 60)
    engine = Engine(600, 600, 'Objective Snake')

    engine.game_loop(the_game)

    engine.quit()
