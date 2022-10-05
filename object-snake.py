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


if __name__ == '__main__':
    engine = Engine(Game(60, 60), 'Objective Snake')
    engine.game_loop()
    engine.quit()
